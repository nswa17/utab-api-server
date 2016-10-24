# TODOs

## Need early fix

1. styles中身確認

1. codeを自動化

1. constants揃ってるか確認

1. verify received round num

1. Error to TextJSON

1. realtime check system -> free from grid_list, lattice_list

1. list all information to send @ apiary

1. define exceptions

1. teamnum and team_num_per_round

1. what if an error occurs when controller is called

1. check received json format

1. round_num -> current_round

1. random test program

1. とりあえずpickleを使ってバックアップを構築

## Do when above finished

1. 無限ラウンド

1. いきなりcheck_allocationが呼ばれた場合, grid_listが完成していない

1. 冗長性をもたせる

1. Integrate grid, lattice

1. Implementing DELETE method

1. lock が働いているか. (thread test)

1. speaker と team 登録の順番を交換可能にする(Noneで登録してラウンド進むときにチェック)

1. don't consider breaknum when breaknum == 0

1. 複数チェアに対応

1. modify result

1. authentication

1. solve state dependencies(make it possible to interrupt allocation selection phase) (チーム配置確定後ジャッジ配置を考えるときにチームを変えられない)

1. use database(mongodb?)

	* back up data instead of db?

	* define getter and setter, change variables `self.x` to `self.__x`

1. modified gale shapley

1. deal with changing round num while tournament <!--  unnecessary? -->

1. choose selection algorithm

1. gini_index

1. rank team every round

1. large warningsをimporove

1. namespace
