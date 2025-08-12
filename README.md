
This is a github repo for manuscript:
"Biofoundry-enabled Investigation of the Combinatorial Effects of Transcription Factors on Free Fatty Acid Synthesis in Saccharomyces cerevisiae"

## Echo_primer_transfer

### Usage

```shell
python echo_primer_transfer.py -i ./data/Batch_2_primer_mix_transfer.csv -o ./results -b batch_2
```

* `-i` the path of the input `*.csv` File
* `-o` the output path of files
* `-b` the output index of files


### Input
example: 

`Batch_2_primer_mix_transfer.csv`:

| Index | Gene |
| ----- | ---- |
| 1     | OPI1 |
| 2     | RFX1 |
| 3     | RGR1 |
| 4     | RPD3 |
| #     | .... |

Only need to input the gene list, primer mix of source plate and volume will be automatically generated.

### Output
examples:

`batch_2_source_plate.csv`

`batch_2_source_vol.csv`:
|   | Gene | Num | NeedWell | NeedVol |
| - | ---- | --- | -------- | ------- |
| 0 | OPI1 | 2   | 1        | 30      |
| 1 | RFX1 | 2   | 1        | 30      |
| 2 | RGR1 | 3   | 2        | 45      |
| 3 | RPD3 | 4   | 2        | 60      |
| 4 | SPT3 | 5   | 2        | 75      |
| 6 | YAP6 | 6   | 3        | 90      |
| 5 | TFC7 | 7   | 3        | 105     |

`batch_2_source2destination_plate.csv`:
|   | 1  | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  | 10 | 11 | 12 |
| - | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- |
| A | A1 | C1 | I1 | B1 | E1 | L1 | G1 | M1 | J1 | J1 | K1 |    |
| B | A1 | E1 | I1 | B1 | G1 | L1 | G1 | F1 | J1 | J1 | M1 |    |
| C | A1 | E1 | L1 | B1 | G1 | C1 | H1 | F1 | M1 | J1 | N1 |    |
| D | B1 | E1 | L1 | C1 | G1 | C1 | I1 | F1 | M1 | M1 | N1 |    |
| E | B1 | G1 | L1 | C1 | I1 | D1 | I1 | H1 | M1 | M1 | N1 |    |
| F | B1 | G1 | A1 | C1 | I1 | E1 | J1 | H1 | H1 | M1 | N1 |    |
| G | C1 | G1 | A1 | E1 | I1 | E1 | L1 | H1 | H1 | J1 | N1 |    |
| H | C1 | I1 | A1 | E1 | L1 | F1 | L1 | J1 | H1 | K1 |    |    |

`batch_2_source2destination_transfer.csv`



## Fluent Worklist

Please refer to `./Fluent_worklist/Fluent_worklist.ipynb`