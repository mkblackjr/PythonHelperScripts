

def ASCConvert(character):
    ret = []
    high_bits = character>>4
    low_bits = character&0xF
    if high_bits<10:
        ret.append( high_bits + 48 )
    else:
        ret.append( high_bits + 55 )

    if low_bits<10:
        ret.append( low_bits + 48 )
    else:
        ret.append( low_bits + 55 )

    return ret


if __name__ == "__main__":
    print("{} = {}".format('A', ASCConvert(65) ))
    print("{} = {}".format('a', ASCConvert(97) ))
    print("{} = {}".format('255', ASCConvert(255) ))
    print("{} = {}".format('23', ASCConvert(23) ))
    print("{} = {}".format('45', ASCConvert(45) ))
    print("{} = {}".format('128', ASCConvert(128) ))






