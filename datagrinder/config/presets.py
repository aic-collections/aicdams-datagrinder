si_defaults = {
    "format": "jpeg",
    "resize": False,
    "resolution" : "96x96",
    "crop": False,
    "color_space": "RGB",
    "color_profile": "sRGB",
    "flatten": True,
    "metadata": "technical",
    "quality": 85,
}

si_settings = {
    "master": {
        "resize": "4096x4096>",
        "quality": 90,
    },
    "int_lg": {
        "resize": "2048x2048>",
    },
    "int_md": {
        "resize": "512x512>",
    },
    "int_thumb": {
        "resize": "128x128>",
        "quality": 75,
        "metadata" : "minimal",
    },
    "citi_thumb": {
        "resize": "96x96>",
        "quality": 75,
        "metadata" : "minimal",
    },
    "web_lg": {
        "resize": "1024x1024>",
        "resolution" : "72x72",
        "metadata": "web",
    },
    "web_md": {
        "resize": "512x512>",
        "resolution" : "72x72",
        "metadata": "web",
    },
    "web_thumb": {
        "resize": "128x128>",
        "resolution" : "72x72",
        "quality": 75,
        "metadata" : "minimal",
    },
}

## exiftool presets to strip or maintain metadata sets
#  Each preset has a 'preserve' and a 'remove' list. Each list contains keywords used
#  to build the exiftool command line. The 'preserve' option trumps the 'remove'one.
#  See `man 1 exiftool`, "WRITING EXAMPLES" section.
si_metadata_presets = {
    'all' : False, # This is a special case that skips the exiftool execution.
    'technical' : {
        'preserve' : [
            'FILE:all',
            'EXIF:all',
            'XMP:all',
            'ICC_Profile:all'
        ],
        'remove' : ['all']
    },
    'web' : {
        'preserve' : [
            'FILE:all',
            'EXIF:all',
            'XMP:ICCProfileName',
            'XMP:ColorSpace',
            'ICC_Profile:all',
        ],
        'remove' : ['all']
    },
    'minimal' : {
        'preserve' : [
            'EXIF:ImageWidth',
            'EXIF:ImageHeigh',
            'EXIF:DocumentName',
            'EXIF:XResolution',
            'EXIF:YResolution',
            'EXIF:Orientation',
            'XMP:ICCProfileName',
            'XMP:ColorSpace',
            'ICC_Profile:DeviceModel',
            'ICC_Profile:ProfileDescription',
            'ICC_Profile:DeviceModelDesc',
        ],
        'remove' : ['all']
    },
    'profile_only' : {
        'preserve' : [
            'XMP:ICCProfileName',
            'XMP:ColorSpace',
            'ICC_Profile:DeviceModel',
            'ICC_Profile:ProfileDescription',
            'ICC_Profile:DeviceModelDesc',
        ],
        'remove' : ['all']
    },
    'none' : {
        'preserve' : [],
        'remove' : ['all']
    },
}


## Merge defaults with each setting
si_presets = {}
for pname in si_settings.keys():
    si_presets[pname] = dict(list(si_defaults.items()) + list(si_settings[pname].items()))
