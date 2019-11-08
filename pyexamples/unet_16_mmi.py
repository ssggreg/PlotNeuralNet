import sys

sys.path.append('../')
from pycore.tikzeng import *
from pycore.blocks import *

arch = [
    to_head('..'),
    to_cor(),
    to_begin(),

    # input
    to_input('../examples/fcn8s/brain_test.png'),

    # block-001
    to_ConvConvRelu(name='ccr_b1', s_filer=160, n_filer=(3, 16), offset="(0,0,0)", to="(0,0,0)", width=(5, 5),
                    height=40, depth=40),
    to_Pool(name="pool_b1", offset="(0,0,0)", to="(ccr_b1-east)", width=1, height=32, depth=32, opacity=0.5),

    *block_2ConvPool(name='b2', botton='pool_b1', top='pool_b2', s_filer=80, n_filer=(16, 32), offset="(1,0,0)",
                     size=(32, 32, 4), opacity=0.5),
    *block_2ConvPool(name='b3', botton='pool_b2', top='pool_b3', s_filer=40, n_filer=(32, 64), offset="(1,0,0)",
                     size=(25, 25, 3), opacity=0.5),
    *block_2ConvPool(name='b4', botton='pool_b3', top='pool_b4', s_filer=20, n_filer=(64, 128), offset="(1,0,0)",
                     size=(16, 16, 2.6), opacity=0.5),
    # Decoder

    to_conc(name='c5', to='pool_b4', offset="(1.2,0,0)"),
    *block_Unconv_2(name="b6", botton='c5', top='end_b6', s_filer=40, n_filer=(192, 64), offset="(1.5,0,0)",
                    size=(25, 25, 3), opacity=0.3),
    to_conc(name='c6', to='end_b6', offset="(1.7,0,0)"),

    *block_Unconv_2(name="b7", botton="c6", top='end_b7', s_filer=80, n_filer=(96, 32), offset="(1.5,0,0)",
                    size=(32, 32, 4), opacity=0.3),
    to_conc(name='c7', to='end_b7', offset="(1.9,0,0)"),

    *block_Unconv_2(name="b8", botton="c7", top='end_b8', s_filer=160, n_filer=(48, 16), offset="(1.8,0,0)",
                    size=(40, 40, 5), opacity=0.3),
    *block_Unconv_k1(name="b9", botton="end_b8", top='end_b9', s_filer=160, n_filer=(16, 2), offset="(3.2,0,0)",
                     size=(40, 40, 5), opacity=0.5),

    to_ConvSoftMax(name="soft1", s_filer=160, offset="(3,0,0)", to="(end_b9-east)", width=0.1, height=40, depth=40,
                   caption="SOFTMAX"),
    to_connection_interpole('pool_b4', 'c5'),
    to_connection_interpole('end_b6', 'c6'),
    to_connection_interpole('end_b7', 'c7'),
    to_skip(of='ccr_b3', to='c5', pos=1.25, h=5.5),
    to_skip(of='ccr_b2', to='c6', pos=1.25, h=7.25),
    to_skip(of='ccr_b1', to='c7', pos=1.25, h=9.25),

    to_connection("end_b9", "soft1"),

    to_input('../examples/fcn8s/brain_rez.png', to="(35,0,0)"),

    to_end()
]


def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex')


if __name__ == '__main__':
    main()
