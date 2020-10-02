#!/bin/bash

repo_name=${PWD##*/}

gh pr create --title "Improvement: Remove pubspec.lock" --body "According to Google Dart guidelines: <br></br> > For library packages, don’t commit the pubspec.lock file. Regenerating the pubspec.lock file lets you test your package against the latest compatible versions of its dependencies.<br>https://dart.dev/guides/libraries/private-files#pubspeclock <br><br>In that sense, since $repo_name is a package, \`pubspec.lock\` should be removed" --head "freitzzz:improvement/remove-pubspec-lock"
