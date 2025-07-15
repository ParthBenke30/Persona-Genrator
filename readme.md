# Reddit User Persona Generator

This tool takes a Reddit profile URL, scrapes recent posts and comments, and creates a user persona. It includes sentiment analysis, personality guess (MBTI-style), and favorite interests with source citations.

##  Files Included

- `reddit_persona_generator.py`: Main script
- `persona_kojied.txt`: Example persona
- `persona_Hungry-Move-6603.txt`: Example persona
- `README.md`: You're reading it!

##  How to Use

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/reddit-persona-generator.git
   cd reddit-persona-generator

2. Run the Python script:
   ```bash
   python reddit_persona_generator.py

3. Enter a valid Reddit profile URL when prompted:  
   ```bash
   Enter Reddit profile URL (e.g., https://www.reddit.com/user/example_user/):

The script will create two files in the same folder:

persona_<username>.txt
persona_<username>.html


| File/Folder                    | Description                                               |
| ------------------------------ | --------------------------------------------------------- |
| `reddit_persona_generator.py`  | Main script that performs scraping and persona generation |
| `persona_kojied.txt`           | Sample persona output for Reddit user `kojied`            |
| `persona_Hungry-Move-6603.txt` | Sample persona for `Hungry-Move-6603`                     |
| `persona_*.html`               | HTML version of persona with links                        |
| `README.md`                    | Setup instructions and documentation                      |

