Persona Generator
This project is a Python-based Reddit user persona generator that scrapes a Reddit user's recent posts and comments to infer their interests. The tool creates both a text and HTML persona file, with each inferred interest citing the original post or comment it came from.

Installation
Clone the repository

Make sure Python 3.7+ is installed

Run: pip install requests

Usage
Run the script: python reddit_persona_generator.py
Input a Reddit profile URL like: https://www.reddit.com/user/example_user/
View generated files: persona_<username>.txt and persona_<username>.html
Features
Scrapes latest Reddit posts/comments
Detects user interests and hobbies
Cites sources for each trait
Creates TXT and HTML reports
Output/Example
Sample output files:

persona_kojied.txt
persona_Hungry-Move-6603.html
Files
reddit_persona_generator.py - Main script
persona_<username>.txt - Text output of persona
persona_<username>.html - Styled HTML report
README.md - This file
