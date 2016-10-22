# TODOs

## Need early fix

* resource_url が変数を使えるようにする

* list all information to send @ apiary

* integrate panel allocation and judge allocaion

* define exceptions

* Lock for api server <--! single thread is much better?-->

* teamnum and team_num_per_round

* what if an error occurs when controller is caled

* check received json format

* round_num -> current_round

* random test program

## Do when above finished

* candidate -> suggested

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

* large warnings の efficiency imporove!