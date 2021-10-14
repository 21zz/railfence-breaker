# Railfence Bruteforce
Currently not that efficient. Use `python break.py -h` for help
## Requirements
can find them in the requirements.txt and install with `pip install -r requirements.txt`.

if you can't figure that out, then they are the following:
* colorama >= 0.4.4
* dephell-argparse  >=0.1.3
* pathos >= 0.2.8
* pyenchant >= 3.2.1

and if you cant figure that out, type `pip install colorama argparse pathos pyenchant` 

<br/>

there are some other requirements for running this
### Windows
 * linux (kidding, should be ok)
### Linux
 * Get the [enchant](https://abiword.github.io/enchant/) library for your distro
 * [Hunspell](https://hunspell.github.io/) or [Nuspell](https://nuspell.github.io/)
 * maybe other stuff i cant be bothered listing right now
## TODO
* detect correct answer before finishing all threads
  * theoretically, this should cut average times in half
* move solution verifying to same thread as offset/rail checking to reduce memory usage
  * Remove stupid full_solution, since that's most of the memory footprint. only fill with useful information
* print solution along side of %correctness

## credit
 * [tothi](https://github.com/tothi) for making [railfence in python](https://github.com/tothi/railfence)
 * [rumkin](http://rumkin.com/tools/cipher/railfence.php) for the inspiration
 * me