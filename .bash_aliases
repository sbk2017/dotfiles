alias btc="python3 /home/sultan/Projects/Btc/btcprice.py"
alias backup="python3 /home/sultan/Projects/Backup/bkr.py backup"
alias restore="python3 /home/sultan/Projects/Backup/bkr.py restore"
#alias -s py=nvim
#alias -s txt=nvim
#alias rdd="rm -rf"
alias gh="cd ~"
alias gd="cd ~/Downloads"
#alias cashflow="python3 ~/Projects/cashflow/cashflow.py"
alias m="urxvt -e man"
alias vpn="python3 ~/Projects/vpn/try_vpn.py"
alias acc="cd ~/Documents/Personal/Accounts/2021/ && subl general.beancount"
alias cashflow="python3 ~/Documents/Personal/Accounts/scripts/myquery.py cashflow"
alias income="python3 ~/Documents/Personal/Accounts/scripts/myquery.py income"
alias due="python3 ~/Documents/Personal/Accounts/scripts/myquery.py duedate"
alias bal="python3 ~/Projects/binance/mybinance.py bal"
alias orders="python3 ~/Projects/binance/mybinance.py orders"
alias trades="python3 ~/Projects/binance/trades.py"
alias help="python3 -m rich.markdown ~/Projects/pages/help.md"
alias movies="cd ~/Projects/MoviesList/ && python3 appgui.py"
zipfile () {
    zip $1 $(cat $2)
}
zipdir () {
    zip -r $1 $(cat $2)
}

