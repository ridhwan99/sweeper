import click, time
from settings import MyAccount

@click.command()
@click.option('--walletA', '-wA', 'walletA', type=str, help='Parent wallet')
@click.option('--walletB', '-wB', 'walletB', type=str, help='Child wallet')
@click.option('--chain', '-ch', 'chain', type=click.Choice(['eth', 'pulsechain']), help='Network', default='pulsechain')
def sweep(walletA, walletB, chain):
    acc = MyAccount(ethWalletAddress=walletA, walletBAddress=walletB, chain=chain)
    while True:
        try:
            acc.send_max_eth(acc.walletBAddress)
        except Exception as e:
            print(e)
            time.sleep(30)
