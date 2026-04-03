# Buildozer spec for Road Rush
[app]

# App identity
title = Road Rush
package.name = roadrush
package.domain = org.roadrush

# Source — main.py must be the entry point
source.dir = .
source.include_exts = py,png,jpg,jpeg,gif,bmp,wav,ogg,mp3
source.exclude_dirs = __pycache__, build, dist, .git, .github, .buildozer, RoadRush.spec

# Version
version = 1.0

# Requirements for a pure-pygame Android app
# python3, sdl2, pygame are all available as p4a recipes
requirements = python3,sdl2,pygame

# Orientation
orientation = portrait

# Android settings
android.permissions = VIBRATE
android.archs = arm64-v8a, armeabi-v7a
android.bootstrap = sdl2
android.minapi = 21
android.sdk = 34
android.ndk = 25b
android.ndk_api = 21
android.accept_sdk_license = True
android.skip_update = False

# Fullscreen
fullscreen = 1

[buildozer]
log_level = 2
warn_on_root = 1
