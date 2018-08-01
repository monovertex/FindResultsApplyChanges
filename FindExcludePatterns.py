import sublime_plugin, sublime
import re

class FindExcludePatternsOMG(sublime_plugin.EventListener):

    def on_window_command(self, window, command_name, args):
        if command_name == 'show_panel' and 'panel' in args and args['panel'] == 'find_in_files' and 'FindExcludePatternsOMG' not in args:
            exclude = self.get_exclude_patterns()
            print(exclude)

            for k, v in enumerate(exclude):
                exclude[k] = exclude[k].replace('\\', '/')
            exclude = sorted(exclude)

            if 'where' in args and args['where']:
                where = args['where']
                where = where.replace('\\', '/')
                where = where.replace('*', '')
                where = re.sub('([a-z])\:/', '', where, 0, re.I)
                where = re.sub('/$', '', where)
                new_exclude = []
                for item in exclude:
                    thingy = item
                    thingy = thingy.replace('-*', '')
                    thingy = thingy.replace('*', '')
                    thingy = re.sub('([a-z])\:/', '', thingy, 0, re.I)
                    thingy = re.sub('-/([a-z])\/', '', thingy, 0, re.I)
                    thingy = re.sub('/$', '', thingy)
                    if thingy not in where:
                        new_exclude.append(item)
                args['where'] = args['where'] + ',' + ('-'+(',-'.join(new_exclude)))
            else:
                args['where'] = '-'+(',-'.join(exclude))

            args['where'] = re.sub('([a-z])\:/', '/\\1/', args['where'].replace('\\', '/'), 0, re.I)
            args['FindExcludePatternsOMG'] = 1

            return (command_name, args)

    def get_exclude_patterns(self):
        index_exclude_patterns = self.get_setting('index_exclude_patterns')
        binary_file_patterns = self.get_setting('binary_file_patterns')
        print(index_exclude_patterns, binary_file_patterns)
        return list(set(list(index_exclude_patterns + binary_file_patterns)))

    def get_setting(self, setting):
        project_settings = sublime.active_window().active_view().settings()
        sublime_settings = sublime.load_settings('Preferences.sublime-settings')
        project_setting = project_settings.get(setting, [])
        sublime_setting = sublime_settings.get(setting, [])
        return project_setting + sublime_setting
