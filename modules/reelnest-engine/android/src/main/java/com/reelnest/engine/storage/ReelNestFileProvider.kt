package com.reelnest.engine.storage

import androidx.core.content.FileProvider

/** Own subclass so the manifest merger never collides with another library's FileProvider entry. */
class ReelNestFileProvider : FileProvider()
