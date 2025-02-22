# Youtube search and download video

## Overview

This Python module provides the ability to find videos from YouTube using flexible search and also download them.

## Features

- Flexible service configuration using json
- Find videos on YouTube
- Download video


## Requirements

- Python 3.10
- pytubefix
- google-api-python-client

## Installation

```bash
pip install -r .../requirements/req.txt
```

## Configuration
Before searching and downloading videos, you need to configure paths and json.
Set up paths in Jupiter and complete the first two cells. Then go to settings.json.  
You will see a configuration like this:

```bash
{
  "type": "search",
  "query_settings": {
    "query": [],
    "exclude": [],
    "max_count": 10,
    "page_count": {
      "first": 0,
      "last": 10
    },
    "region_code": "UA",
    "published_after": {
      "year": 2000,
      "month": 1,
      "day": 1
    },
    "published_before": {
      "year": 2030,
      "month": 1,
      "day": 1
    }
  },
  "json_path": "./data/video_paths.json",
  "download_folder_path": "./data/video",
  "max_threads": 4,
  "api_key": ""
}
```
A little about each setting:
- **Type** is a service selection. Available: "search" or "download"
- **Queries** are presented as an array. You can write several queries at once for wide coverage. Example:
  - ["dogs", "cats"] will find you N videos with dogs and N videos with cats. 
  - ["dogs cats"] should find you N videos in which there will be both cats and dogs.
- **Exclude**: list all the words that should not appear in response.
- **Max_count**: maximum number of answers (videos) per page.
- **Page_count**: first and last pages for search.
- **Json_path**: file with all found videos.
- **Api_key**: key that is generated in Google cloud console (YouTube Data API v3)

## Download
After setting up, execute the code with the "search" **type**.
After you have found the videos, view the ones you need and set the flag = 1 for the videos you want to download.  
Go to configuration, change **type** from "search" to "download" and run again. Repeat until you achieve the desired result.