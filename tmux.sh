# 创建一个名为 train 的新会话
tmux new -s train

# 退出当前会话，回到之前的 bash 中 | ctrl+b，再按下d（detach）
tmux detach

# 回到train这个会话中
tmux attach -t train

# tmux ls命令可以查看当前所有的 Tmux 会话。
tmux ls
# train: 1 windows (created Fri May  7 03:01:42 2021) [130x44]
# 注意 如果在session中使用exit，这个session就会被关闭

# 删除名为train的会话
tmux kill-session -t train
