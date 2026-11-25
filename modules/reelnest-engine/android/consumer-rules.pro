# ProGuard / R8 rules for ReelNest Engine
# JNI: Rust looks these classes and methods up by name.
-keep class com.reelnest.engine.NativeCore { *; }
-keepclassmembers class * {
    native <methods>;
}
-keep class com.reelnest.engine.ReelNestEngineModule { *; }
-keep class com.reelnest.engine.service.ReelNestTorrentService { *; }
-keep class com.reelnest.engine.storage.ReelNestFileProvider { *; }
