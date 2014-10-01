si_defaults = {
	"format": "jpeg",
	"resize": False,
	"crop": False,
	"color_space": "RGB",
	"color_profile": "sRGB",
	"flatten": True,
	"metadata": "used",
	"quality": 85,
}

si_settings = {
	"master": {
		"resize": "4096x4096",
		"quality": 90,
	},
	"int_lg": {
		"resize": "2048x2048",
	},
	"int_md": {
		"resize": "512x512",
	},
	"int_thumb": {
		"resize": "128x128",
		"quality": 75,
	},
	"citi_thumb": {
		"resize": "96x96",
		"quality": 75,
	},
	"web_lg": {
		"resize": "1024x1024",
		"metadata": "web",
	},
	"web_md": {
		"resize": "512x512",
		"metadata": "web",
	},
	"web_thumb": {
		"resize": "128x128",
		"metadata": "web",
		"quality": 75,
	},
}


## Merge defaults with each setting
si_presets = {}
for pname in si_settings.keys():
	si_presets[pname] = dict(list(si_defaults.items()) + list(si_settings[pname].items()))
