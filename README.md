# update-notifier
A small web application to monitor pwman3 versions

This application is meant to notify pwman3 versions about newer versions.

When Pwman3 starts it qeueries this app for the latest versions available.
This app will ask pypi and\or github for the latest versions.

The reason why Pwman3 does not do it directly is that I don't want to
add dependencies to Pwman3 and I would also like to gather statistics of usage.

Everyone interested can opt-out, and NOTHING will be sent from pwman3 besides the actual
version used EVER.
