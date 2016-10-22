# TODOs

## Need early fix

* adj_name janakute adj_id @apiary

* adjudicator_id comments @apiary

* all adj/speaker results @ apiary

* all -> total @ apiary

* add debater @apiary

* (judge_criteria -> )judge_criterion @ apiary

* tournament code @apiary

* modify candidate allocation ? @apiary @kym

	* remote check allocations (@apiary)

* list all information to send @ apiary

* integrate panel allocation and judge allocaion

* matchup -> team allocation

* define exceptions

* Lock for api server <--! single thread is much better?-->

* teamnum and team_num_per_round

* what if an error occurs when controller is caled

* check received json format

* create_tournament のところ修正

* round_num と num_of_rounds統一

## Do when above finished

* thread test

* speaker と team 登録の順番を交換可能にする

* don't consider breaknum when breaknum == 0

* multiple judges

* modify result

* authentication

* solve state dependencies(make it possible to interrupt allocation selection phase)

* use database(mongodb?)

	* back up data instead of db?

	* define getter and setter, change variables self.* to self.__*

* modified gale shapley

* deal with changing round num while tournament

* choose selection algorithm

* gini_index

* rank team every round