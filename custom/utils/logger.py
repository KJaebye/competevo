import math
from lib.utils.stats_logger import StatsLogger
from lib.rl.core.logger_rl import LoggerRL


class LoggerRLV1(LoggerRL):

    def __init__(self, init_stats_logger=True, use_c_reward=False):
        super().__init__(init_stats_logger, use_c_reward)
        self.stats_names += ['exec_reward', 'exec_episode_reward']
        if init_stats_logger:
            self.stats_loggers['exec_reward'] = StatsLogger()
            self.stats_loggers['exec_episode_reward'] = StatsLogger()

    def start_episode(self, env):
        super().start_episode(env)
        self.exec_episode_reward = 0

    def step(self, env, reward, c_reward, c_info, info):
        super().step(env, reward, c_reward, c_info, info)
        if info['stage'] == 'execution':
            self.stats_loggers['exec_reward'].log(reward)
            self.exec_episode_reward += reward

    def end_episode(self, env):
        super().end_episode(env)
        self.stats_loggers['exec_episode_reward'].log(self.exec_episode_reward)

    def end_sampling(self):
        super().end_sampling()

    @classmethod
    def merge(cls, logger_list, **kwargs):
        logger = super().merge(logger_list, **kwargs)
        logger.avg_exec_reward = logger.stats_loggers['exec_reward'].avg()
        logger.avg_exec_episode_reward = logger.stats_loggers['exec_episode_reward'].avg()
        return logger

class MaLoggerRLV1:
    def __init__(self, learner_num, **kwargs) -> None:
        self.loggers = [LoggerRLV1(**kwargs) for _ in range(learner_num)]

    @classmethod
    def merge(cls, loggers_list, **kwargs):
        loggers_list = list(map(list, zip(*loggers_list)))
        loggers = []
        for i in range(len(loggers_list)):
            """ i means the ith agent's logger. """
            logger_i_list = loggers_list[i]
            loggers.append(LoggerRLV1.merge(logger_i_list, **kwargs))
        return loggers
    
class MaLoggerRL:
    def __init__(self, learner_num, **kwargs) -> None:
        self.loggers = [LoggerRL(**kwargs) for _ in range(learner_num)]

    @classmethod
    def merge(cls, loggers_list, **kwargs):
        loggers_list = list(map(list, zip(*loggers_list)))
        loggers = []
        for i in range(len(loggers_list)):
            """ i means the ith agent's logger. """
            logger_i_list = loggers_list[i]
            loggers.append(LoggerRL.merge(logger_i_list, **kwargs))
        return loggers