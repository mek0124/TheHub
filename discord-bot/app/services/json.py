import json
import os


class JsonEngine:
    def check_exists(self, file_name: str = "config.json"):
        curr_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
        app_dir = os.path.dirname(curr_dir)
        data_dir = os.path.join(app_dir, "data")

        if not os.path.isdir(data_dir):
            os.mkdir(data_dir)

        return_file = os.path.join(data_dir, file_name)

        if not os.path.isfile(return_file):
            default_data = {
                "token": "",
                "guildId": 0
            }

            with open(return_file, 'w+', encoding="utf-8-sig") as new:
                json.dump(default_data, new, indent=2)

            return return_file
        
        return return_file
            
    def get_rules(self):
        rules_file = self.check_exists("rules.json")

        with open(rules_file, 'r', encoding="utf-8-sig") as f:
            data = json.load(f)

            return data
        
    def get_all_commands(self):
        commands_file = self.check_exists("commands.json")

        with open(commands_file, 'r', encoding="utf-8-sig") as f:
            data = json.load(f)

            return (data["general"], data["mods"], data["admins"], data["devs"], data["owner"])
        
    def get_greetings(self):
        """
        A function for the engine to retrieve the list of
        greetings from the greetings file
        """
        greetings_file = self.check_exists("greetings.json")

        with open(greetings_file, 'r', encoding="utf-8-sig") as f:
            data = json.load(f)

            return data
