#!/usr/bin/python2
# -*- coding: utf-8 -*-
import json
import cgi
# import cgitb; cgitb.enable()
import sys
import jinja2
import os
import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm

email = os.getenv("SSL_CLIENT_S_DN_Email")
if email is None or not email.lower().endswith("@mit.edu") or email.count("@") != 1:
    print("Content-type: text/plain\n")
    print("Valid MIT certificate with @mit.edu address required.")
    sys.exit(0)
kerberos = email[:email.index("@")]

SQLBase = sqlalchemy.ext.declarative.declarative_base()

class Pronouns(SQLBase):
    __tablename__ = "pronouns"
    kerberos = sqlalchemy.Column(sqlalchemy.String(63), nullable=False, primary_key=True)
    substitute = sqlalchemy.Column(sqlalchemy.String(63), nullable=True)
    pronouns = sqlalchemy.Column(sqlalchemy.Text(), nullable=False)
    last_updated = sqlalchemy.Column(sqlalchemy.TIMESTAMP(), nullable=False)
    revision = sqlalchemy.Column(sqlalchemy.Integer(), nullable=False)

with open(os.path.join(os.getenv("HOME"), ".my.cnf")) as f:
    password = dict(line.strip().split("=") for line in f if line.count("=") == 1)["password"]

sqlengine = sqlalchemy.create_engine("mysql://cela:%s@sql.mit.edu/cela+pronouns" % password)
SQLBase.metadata.bind = sqlengine

session = sqlalchemy.orm.sessionmaker(bind=sqlengine)()
fetched = session.query(Pronouns).all()

class CGILoader(jinja2.BaseLoader):
    def get_source(self, environment, template):
        template = os.path.normpath(template)
        if "/" in template or not os.path.exists(template) or os.path.isdir(template) or not (template.endswith(".py") or template.endswith(".html")):
            raise jinja2.TemplateNotFound(template)
        with open(template) as f:
            source = f.read()
        if source.startswith("#") and "\n" in source:
            source = source[source.index("\n"):]
        return source, template, lambda: True

class Object: pass

def format_pronouns(pronouns):
    obj = Object()
    if pronouns is None:
        return None
    else:
        assert type(pronouns) == list and len(pronouns) == 6
        return pronouns

they_them = ["they", "them", "their", "theirs", "themself", True]

def parse_line(line):
    obj = Object()
    obj.kerberos = line.kerberos
    obj.substitute = line.substitute
    obj.vkerb = line.substitute if line.substitute else line.kerberos
    pronouns = json.loads(line.pronouns)
    version = pronouns.get("version", 1)
    obj.names = pronouns.get("names", [])
    obj.preferred = format_pronouns(pronouns.get("primary", None))
    obj.accepted = [format_pronouns(prs) for prs in pronouns["accept"]]
    obj.accept_nothey = obj.accepted[:]
    if they_them in obj.accepted:
        obj.accept_nothey.remove(they_them)
    obj.accept_they = they_them == obj.preferred or they_them in obj.accepted
    obj.prefixes = pronouns.get("prefixes", [])
    return obj
empty_user_object = Object()
empty_user_object.kerberos = kerberos
empty_user_object.substitute = None
empty_user_object.vkerb = kerberos
empty_user_object.names = []
empty_user_object.preferred = None
empty_user_object.accepted = []
empty_user_object.accept_nothey = []
empty_user_object.accept_they = True
empty_user_object.prefixes = []

def redirect(target):
    print("Content-type: text/plain")
    print("Location: %s\n" % target)
    print("Redirecting...")
actions = {}
def update_pronouns():
    form = cgi.FieldStorage()
    prefixes = form.getvalue("prefixes", [])
    if type(prefixes) != list:
        prefixes = [prefixes]
    else:
        prefixes = [prefix for prefix in prefixes if prefix.strip()]
    names = form.getvalue("names", [])
    if type(names) != list:
        names = [names]
    else:
        names = [name for name in names if name.strip()]
    names = [name.strip() for name in ",".join(names).split(",") if name.strip()]
    pronouns = []
    i = 0
    while True:
        pronoun_set = [form.getvalue("pr%d_%d" % (i, j), "").strip() for j in range(5)]
        if not any(pronoun_set):
            if i == 0:
                pronouns.append(None)
            else:
                break
        else:
            is_plural = form.getvalue("pr%d_p" % i) == "on"
            pronouns.append(pronoun_set + [is_plural])
        i += 1
    if pronouns[0] in pronouns[1:]:
        pronouns = [pronouns[0]] + [x for x in pronouns[1:] if x != pronouns[0]]
    if they_them not in pronouns and form.getvalue("prthey", ""):
        pronouns.insert(1, they_them)
    pronoun_json = json.dumps({"version": 1, "names": names, "primary": pronouns[0], "accept": pronouns[1:], "prefixes": prefixes})
    if session.query(Pronouns).filter(Pronouns.kerberos == kerberos).count() == 0:
        # does not yet exist
        new_row = Pronouns(kerberos=kerberos, substitute=None, pronouns=pronoun_json, revision=1)
        session.add(new_row)
    else:
        # already exists
        old_row = session.query(Pronouns).filter(Pronouns.kerberos == kerberos).one()
        old_row.pronouns = pronoun_json
        old_row.revision += 1
        session.add(old_row)
    session.flush()
    session.commit()
    redirect(".")
actions["update.py"] = update_pronouns

source = sys.argv[1] if sys.argv[1:] else "index.py"
if source == "action":
    s2 = os.path.normpath(sys.argv[2]) if sys.argv[2:] else ""
    if s2 in actions:
        actions[s2]()
    else:
        print("Content-type: text/plain\n")
        print("Invalid action.")
else:
    env = jinja2.Environment(loader=CGILoader(), optimized=False, autoescape=True, auto_reload=False)
    env.globals["mapf"] = map
    env.globals["enumerate"] = enumerate
    env.globals["len"] = len
    print("Content-type: text/html\n")
    fetched = [parse_line(line) for line in fetched]
    print(env.get_template(source).render(kerberos=kerberos, fetched=fetched, user={line.kerberos: line for line in fetched}.get(kerberos, empty_user_object)).encode("utf-8"))
