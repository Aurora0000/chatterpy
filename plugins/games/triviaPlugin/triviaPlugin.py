from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManagerSingleton
import logging, string
# The python file's name must be the same as the .chatter file's module attribute
class triviaPlugin(IPlugin):
    def botmsg(self, user, channel, task, args):
        user = user.split("!")[0]
        if task == "quiz":
            if args[0] == "join":
                if user in self.CURRENT_PLAYERS:
                    return
                manager = PluginManagerSingleton.get()
                self.CURRENT_PLAYERS.append(user)
                manager.app.msg(self.CHANNEL, "Once all users are ready, type !quiz start")

            elif args[0] == "start":
                manager = PluginManagerSingleton.get()
                self.QUIZ_STARTED = True
                self.CURRENT_PLAYER = self.CURRENT_PLAYERS[0]
                self.get_questions()
                (self.QUESTION, self.ANSWER) = self.get_question()
                manager.app.msg(self.CHANNEL, "{}: {} | Answer with !quiz answer <answer>".format(self.CURRENT_PLAYER, self.QUESTION))
                
            elif args[0] == "prepare":
                manager = PluginManagerSingleton.get()
                self.CHANNEL = str(manager.app.plugin_get_setting("triviaPlugin", "channel"))
                manager.app.join(self.CHANNEL)
                self.CURRENT_PLAYERS = []
                self.SCORE = {}
                manager.app.msg(channel, "Join {} and say !quiz join to join.".format(self.CHANNEL))

            elif args[0] == "answer":
                if not self.QUIZ_STARTED:
                    return
                manager = PluginManagerSingleton.get()
                ans = string.join(args[1:])
                if user != self.CURRENT_PLAYER:
                    manager.app.msg(self.CHANNEL, "It's not your turn!")
                    return

                if self.ANSWER.lower() == ans.lower():
                    manager.app.msg(self.CHANNEL, "Correct!")
                    self.give_point(user)
                else:
                    manager.app.msg(self.CHANNEL, "Incorrect!")
                self.new_question()

    def get_leaderboard(self):
        manager = PluginManagerSingleton.get()
        scores = [(v, k) for (k, v) in self.SCORE.items()]
        _sorted = [(k, v) for (v, k) in sorted(scores, reverse=True)]
        manager.app.msg(self.CHANNEL, "LEADERBOARD:")
        for items in _sorted:
            manager.app.msg(self.CHANNEL, "{}: {} points".format(items[0], str(items[1])))

    def new_question(self):
        manager = PluginManagerSingleton.get()
        self.CURRENT_PLAYER = self.get_current_user()
        (self.QUESTION, self.ANSWER) = self.get_question()
        if self.QUIZ_STARTED == False:
            manager.app.msg(self.CHANNEL, "Quiz ended!")
            return
        manager.app.msg(self.CHANNEL, "{}: {} | Answer with !quiz answer <answer>".format(self.CURRENT_PLAYER, self.QUESTION))

    def give_point(self, user):
        try:
            self.SCORE[user] = self.SCORE[user] + 1
        except:
            self.SCORE[user] = 1
    
    def get_current_user(self):
        i = self.CURRENT_PLAYERS.index(self.CURRENT_PLAYER)
        try:
            return self.CURRENT_PLAYERS[i + 1]
        except:
            return self.CURRENT_PLAYERS[0]

    def get_question(self):
        if len(self.QUESTIONS) == 0:
            self.QUIZ_STARTED = False
            self.get_leaderboard()
            return (None, None)
        q = self.QUESTIONS[0]
        self.QUESTIONS.remove(q)
        return q

    def get_questions(self):
        manager = PluginManagerSingleton.get()
        q = manager.app.plugin_get_setting("triviaPlugin", "questions")
        self.QUESTIONS = [(k, v) for (k, v) in q.items()]

