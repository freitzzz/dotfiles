#!/bin/bash

git checkout -b improvement/remove-pubspec-lock

rm pubspec.lock

git add pubspec.lock

git commit -m "Removed pubspec.lock to match Dart guidelines https://dart.dev/guides/libraries/private-files#pubspeclock"

git push --set-upstream origin improvement/remove-pubspec-lock
