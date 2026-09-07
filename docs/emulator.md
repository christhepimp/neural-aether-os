# Emulator and Linux-inside-Android notes

## Recommended path: Android Studio AVD without Play Store

1. Install Android Studio / cmdline-tools and create an AVD using a **Google APIs** system image (not Google Play).
2. Start it:
   ```bash
   emulator @AetherDev -no-snapshot-load
   ```
3. Root the adb daemon:
   ```bash
   adb wait-for-device
   adb root
   adb remount
   adb shell id
   ```
   You want `uid=0(root)`.

## Play Store images: AERoot

Play-flavored AVDs lock `adbd`. Use AERoot:

```bash
pip install aeroot
emulator @YourAVD -qemu -s
aeroot daemon     # elevate adbd so subsequent adb shells are root
```

Source: https://github.com/quarkslab/AERoot

Older cousin: https://github.com/airbus-seclab/android_emuroot

## Getting a Linux *userspace* on the emulator

Root on Android is still Android. To work like Linux:

### A. Stay in Android shell (fastest)
```bash
adb push control-plane /data/local/tmp/aether
adb shell
cd /data/local/tmp/aether
# python may not exist; use the host instead, or ship a static binary later
```

### B. PRoot distro (no extra VM)
On a real device, Termux + `proot-distro` is the usual path.
On emulator, you can still install a userspace tarball and fake-root with proot if you ship the binary.

### C. Real VM beside Android (Podroid-style)
A nested QEMU Alpine/Debian VM is closer to "our OS" because it has its own kernel. Heavier, but honest.

## Host-side Linux (often better than the phone emulator)

If the goal is a new OS, **QEMU on a Linux desktop beats a phone emulator** after Stage 1.
Use the Android emulator only to satisfy the "start from rooted Android" requirement and to test agents that must live next to Android services.

## Safety

These notes are for *your own* AVDs and devices. Do not use privilege-elevation tools against other people's phones.
