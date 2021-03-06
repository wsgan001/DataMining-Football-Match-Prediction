import os
import warnings
import src.util.util as util
import src.application.MachineLearning.MachineLearningAlgorithm as mla
import src.application.MachineLearning.MachineLearningInput as mli
from src.application.MachineLearning.prediction_accuracy.prediction_accuracy import PredictionAccuracy
from src.application.MachineLearning.experiment.experiment_plot import PlotExperiment


def warn(*args, **kwargs):
    pass
warnings.warn = warn


experiments = {
    0: "Simulate bet",
    1: "Find best window size by match representation and ml algorithm",
    2: "Compare mla testing different window sizes",
    3: "Find best ML alg, by window size and match representation",
    4: "Given a predictor, build our personal bet-odds and compare them with the real ones"
}


class Experiment(object):
    def __init__(self, type):
        self.type = type
        self.id = util.get_id_by_time()+"_"+str(self.type)

        self.experiment_dir = util.get_project_directory()+"data/experiments/"+self.id
        os.makedirs(self.experiment_dir,exist_ok=True)

    def run(self, league, complete=True, **params):
        if self.type == 0:
            import src.application.MachineLearning.experiment.experiment_0 as exp_0
            type_evaluation = util.get_default(params, "type_evaluation", 1)
            exp_0.run_experiment_0(self, league, type_evaluation)
        elif self.type == 1:
            import src.application.MachineLearning.experiment.experiment_1 as exp_1
            if complete:
                for ml_train_input_id, ml_train_input_descr in mli.get_input_ids().items():
                    for ml_train_input_representation in mli.get_representations(ml_train_input_id):
                        exp_1.run_experiment_1(self, league, ml_train_input_id, ml_train_input_representation)
            else:
                ml_train_input_id =             util.get_default(params, "ml_train_input_id", 1)
                ml_train_input_representation = util.get_default(params, "ml_train_input_representation", 1)
                del(params["ml_train_input_id"])
                del (params["ml_train_input_representation"])
                exp_1.run_experiment_1(self, league, ml_train_input_id, ml_train_input_representation, **params)

        elif self.type == 2:
            import src.application.MachineLearning.experiment.experiment_2 as exp_2
            ml_train_input_id = util.get_default(params, "ml_train_input_id", 1)
            ml_train_input_representation = util.get_default(params, "ml_train_input_representation", 1)
            exp_2.run_experiment_2(self, league, ml_train_input_id, ml_train_input_representation)
            pass

        elif self.type == 3:
            import src.application.MachineLearning.experiment.experiment_3 as exp_3
            if complete:
                pass
            else:
                ml_train_input_id = util.get_default(params, "ml_train_input_id", 1)
                ml_train_input_representation = util.get_default(params, "ml_train_input_representation", 1)
                ml_train_stages_to_train = util.get_default(params, "ml_train_stages_to_train", 10)
                exp_3.run_experiment_3(self, league, ml_train_input_id, ml_train_input_representation, ml_train_stages_to_train)

        elif self.type == 4:
            import src.application.MachineLearning.experiment.experiment_4 as exp_4
            exp_4.run_experiment_4(self, league)

    def create_plot(self, x, y, file_name, is_accuracy=True, **params):
        p = PlotExperiment(self.type, y, x, **params)
        p.plot(path_file=self.experiment_dir + "/" + file_name, is_accuracy=is_accuracy)


def get_x_y(x_list, y_dict):
    x = []
    y = []
    for x_i in x_list:
        try:
            x.append(x_i)
            y.append(y_dict[x_i])
        except KeyError:
            continue
    return x, y


def get_file_name(params, extension="png", pre=None, post=None):
    file_name = ""
    print(pre)
    if pre:
        file_name += pre+"_"

    for p in params:
        file_name += str(p)+"_"

    file_name = file_name[:-1]
    if post:
        file_name += "_"+post

    return file_name+"."+extension
