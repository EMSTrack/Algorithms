# Run with the yaml file to check it is well formed and has the necessary components.
# Recursively checks if certain keys are present

from sys import argv
import yaml

required_keys = [
    'name',
    {
        'simulator': [
            'type'
        ]

    }

]

def check_yaml(filename):
    file = open (filename, 'r')
    contents = yaml.load(file)


if __name__ == "__main__":
    pass