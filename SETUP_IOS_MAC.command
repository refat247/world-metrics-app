#!/bin/sh
set -eu
npm install
[ -d ios ] || npx cap add ios
npx cap sync ios
npx cap open ios
