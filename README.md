# sweeper
#
{} means use your own data
#
# install
git clone https://github.com/ridhwan99/sweeper.git
#
cd sweeper
#
pip install --editable .
#
create .env file
#
add eth node in .env as INFURA_KEY={eth rpc} 
#
add pls node in .env as pulsechain={pls rpc}
#
add parent wallet and private key in .env as {parent wallet}={private key}
# run
sweep --help
#
sweep -wA {parent wallet} -wB {child wallet} -ch {pulsechain or eth}
# what happens
script moves all eth or pls from parent wallet to child wallet when there is enough to pay gas fee.
#
As long as the script runs no eth or pls can remain in the parent wallet.
