import requests

def register_command():
    url = "https://discord.com/api/v10/applications/1205109511103320094/commands"

    # This is an example CHAT_INPUT or Slash Command, with a type of 1
    json = {
        "name": "blep",
        "type": 1,
        "description": "Send a random adorable animal photo",
        "options": [
            {
                "name": "animal",
                "description": "The type of animal",
                "type": 3,
                "required": True,
                "choices": [
                    {
                        "name": "Dog",
                        "value": "animal_dog"
                    },
                    {
                        "name": "Cat",
                        "value": "animal_cat"
                    },
                    {
                        "name": "Penguin",
                        "value": "animal_penguin"
                    }
                ]
            },
            {
                "name": "only_smol",
                "description": "Whether to show only baby animals",
                "type": 5,
                "required": False
            }
        ]
    }

    headers = {
        "Authorization": "Bot MTIwNTEwOTUxMTEwMzMyMDA5NA.GdXEf3.7dwf1CLFW-l8PdLouuFUjlNMUysK5gmHxfLVJc"
    }

    r = requests.post(url, headers=headers, json=json)

register_command()
