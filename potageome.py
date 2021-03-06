#!/usr/bin/env python3

import argparse
from glob import glob
from association2json import generate_js
import jinja2
import sass
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Minifying the .js and .css with -c option")
    parser.add_argument('-c', action='store_true')
    args = parser.parse_args()

    plants, appartenance, examples, categories, cat_plants, cat_animals, interactions = generate_js("js/data.js")

    minified = ""
    if args.c:
        minified = "min."
        from jsmin import jsmin

        for js_path in sorted(glob("js/*.js")):
            if ".min.js" not in js_path:
                with open(js_path, 'r') as js_file:
                    jsminified = jsmin(js_file.read())
                    jsminified_file = open(js_path.replace('.js', ".min.js"), "w")
                    jsminified_file.write(jsminified)
                    jsminified_file.close()

        print("Minifying the .js et .css")
    else:
        print(".js and .css not minified, use -c option if you wish to compress")

    css = open("css/potageome." + minified + "css", "w")
    css.write(sass.compile(filename='potageome.css.scss', output_style=('compressed' if args.c else "nested")))
    css.close()

    env = jinja2.Environment(loader=jinja2.FileSystemLoader('./'))
    template = env.get_template('potageome_template.html')
    output_from_parsed_template = template.stream(plants=plants,
                                                  examples=examples,
                                                  minified=minified,
                                                  cat_plants=cat_plants,
                                                  cat_animals=cat_animals,
                                                  categories=categories,
                                                  interactions=interactions,
                                                  appartenance=sorted(appartenance.items(),
                                                                      key=lambda pl: plants[pl[0]].lower())
                                                  ).dump('potageome.html')
    print("Application generated.\nOpen the file {0}/potageome.html to open the application.".format(os.getcwd()))
