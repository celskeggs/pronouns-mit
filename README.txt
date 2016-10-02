# Project Overview

This is pronouns@mit, a database for the voluntary storage of gender pronouns,
targeted at the MIT community.

The current site is available at cela.scripts.mit.edu, but that is hopefully
going to change to a more general domain in the future.

This is a practical project focused more on practical usages of pronouns,
names, and other personal specifiers. As such, the goal of the project is not
to create a comprehensive format for detailing identities.

The primary use-cases are:

1. Allowing members of the MIT community to determine the correct pronouns for
   each other without needing to ask explicitly, for interactions via email,
   zephyr, or meatspace.
2. Allowing software that interacts primarily with members of the MIT community
   to autofill emails, messages, and other generated snippets of text with the
   correct honorific, name, and pronoun.
3. Allowing groups in the MIT community to include pronoun information
   alongside name and/or kerberos lists to facilitate correct pronoun use.

Information stored in pronouns@mit is for the use of the MIT community and not
those outside of it. pronouns@mit makes reasonable attempts to prevent access
to its data from outsiders, such as the requirement to supply MIT certificates
to access its website, but does not make any guarantees about the security or
privacy of data submitted to it. It is expected that members of the MIT
community who access the data stored in pronouns@mit will make reasonable
attempts to prevent the data from leaking beyond the community.

Since information submitted to pronouns@mit is, by design, visible to the
entire MIT community, care should be taken to only submit person information
that you are okay with being shared with the rest of the MIT community, and
potentially leaking beyond it.

pronouns@mit is provided on a "best-effort" basis. It runs on the
scripts.mit.edu infrastructure, which does not provide any uptime guarantees,
and is not designed for use in any situations that cannot handle downtime.

# Source Code Overview

The source code is very messy, and is due for a clean-up. Similarly, the user
interface is also very messy and low-quality, and is due for an upgrade.
pronouns@mit welcomes any help in accomplishing these tasks.

The code's design - specifically, the use of cgi script infrastructure instead
of more modern tools - is based on the hosting in use, which is the
scripts.mit.edu system.

To my current knowledge, the infrastructure in use on scripts.mit.edu is based
on Apache mod_python, meaning that you should be able to run your own instance
of this project with a similar setup.

The code is currently hard-coded to be associated with the MIT community, but
is open to adjustments to make it more generic.

No support is guaranteed for this project, but we welcome any suggestions. We
also accept pull requests. Suggestions can be submitted either to our email
list, pronouns@mit [dot] edu, or to our project on GitHub at
https://github.com/celskeggs/pronouns-mit.git.

# Deployment Notes

Make sure that you remove the scripts.mit.edu permissions from the .git folder
if you deploy this directly in an AFS locker.

# License

The software behind pronouns@mit is licensed under the MIT license, of course.
See LICENSE.txt for more info.
