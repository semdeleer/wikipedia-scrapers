# Wikipedia-Scrapers

## Introduction

The project provides a convieent interface to interact with the country leaders API and extract information about country leaders, including their wikipedia paragraphs

## Usage

You have the option to incorporate an API that retrieves wikilinks from the provided links. Upon obtaining the links from the API, you can then retrieve and return the introductory paragraph from the first linked API.

## Requirements

You can find everything in the [requirements.txt](./installation)

### Usage

<ol>
    <code>
    wikscraper = Scraper()
    wikscraper.get_leaders()
    wikscraper.get_wiki_leader()
    wikscraper.get_first_paraf()
    wikscraper.get_paraf_leader()
    wikscraper.set_write_json()
    </code>
</ol>
