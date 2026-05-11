window.BENCHMARK_DATA = {
  "lastUpdate": 1778479203556,
  "repoUrl": "https://github.com/scylladb/coodie",
  "entries": {
    "coodie benchmarks (acsylla)": [
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "12180cbd6ba1fe58767b71f29249f25bfda100e9",
          "message": "fix(ci): restore Copilot CLI for commit body generation with proper error handling\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-02-25T20:58:37+02:00",
          "tree_id": "88189deb7187a7bdcc34f0212767601afc9f02a3",
          "url": "https://github.com/fruch/coodie/commit/12180cbd6ba1fe58767b71f29249f25bfda100e9"
        },
        "date": 1772045983652,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_get_or_create_user",
            "value": 1343.4212448663377,
            "unit": "iter/sec",
            "range": "stddev: 0.0002829601302075249",
            "extra": "mean: 744.3681598912738 usec\nrounds: 369"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_get_or_create_user",
            "value": 2072.224984230636,
            "unit": "iter/sec",
            "range": "stddev: 0.000023190982736560474",
            "extra": "mean: 482.57308333306986 usec\nrounds: 876"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_filter_runs_by_status",
            "value": 996.8525500339047,
            "unit": "iter/sec",
            "range": "stddev: 0.00015815199931585677",
            "extra": "mean: 1.0031573876858602 msec\nrounds: 877"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_filter_runs_by_status",
            "value": 1912.0463162986102,
            "unit": "iter/sec",
            "range": "stddev: 0.00008184887377586664",
            "extra": "mean: 522.9998831491836 usec\nrounds: 813"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_latest_runs",
            "value": 1068.136178482814,
            "unit": "iter/sec",
            "range": "stddev: 0.0008215891073225723",
            "extra": "mean: 936.2102137766785 usec\nrounds: 842"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_latest_runs",
            "value": 2073.9504195842137,
            "unit": "iter/sec",
            "range": "stddev: 0.00003275369296460503",
            "extra": "mean: 482.17160379392305 usec\nrounds: 949"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_list_mutation",
            "value": 1343.94010104519,
            "unit": "iter/sec",
            "range": "stddev: 0.00008549940009143176",
            "extra": "mean: 744.0807809978244 usec\nrounds: 621"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_list_mutation",
            "value": 1034.3894156534661,
            "unit": "iter/sec",
            "range": "stddev: 0.00003104574343592757",
            "extra": "mean: 966.7538983548658 usec\nrounds: 1033"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_batch_events",
            "value": 361.879085472308,
            "unit": "iter/sec",
            "range": "stddev: 0.00013610760378766164",
            "extra": "mean: 2.7633539492752 msec\nrounds: 276"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_batch_events",
            "value": 837.1698353713024,
            "unit": "iter/sec",
            "range": "stddev: 0.00006148109033319511",
            "extra": "mean: 1.1945007545051822 msec\nrounds: 444"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_notification_feed",
            "value": 756.7629046023363,
            "unit": "iter/sec",
            "range": "stddev: 0.00012735023228588265",
            "extra": "mean: 1.321417836310938 msec\nrounds: 672"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_notification_feed",
            "value": 1511.3036516857524,
            "unit": "iter/sec",
            "range": "stddev: 0.00009364631108165629",
            "extra": "mean: 661.6803968445195 usec\nrounds: 824"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_status_update",
            "value": 1200.6629453596356,
            "unit": "iter/sec",
            "range": "stddev: 0.00007273895247366218",
            "extra": "mean: 832.8732088092125 usec\nrounds: 613"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_status_update",
            "value": 1030.1340325200429,
            "unit": "iter/sec",
            "range": "stddev: 0.000026252895458873652",
            "extra": "mean: 970.747464340805 usec\nrounds: 659"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_comment_with_collections",
            "value": 1292.5119259843418,
            "unit": "iter/sec",
            "range": "stddev: 0.00007297536326342523",
            "extra": "mean: 773.6872518514111 usec\nrounds: 675"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_comment_with_collections",
            "value": 2034.9963235705884,
            "unit": "iter/sec",
            "range": "stddev: 0.00003825424884915503",
            "extra": "mean: 491.4013791658394 usec\nrounds: 720"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_multi_model_lookup",
            "value": 734.9736653563251,
            "unit": "iter/sec",
            "range": "stddev: 0.00011634332295195219",
            "extra": "mean: 1.3605929669809143 msec\nrounds: 636"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_multi_model_lookup",
            "value": 914.5509992532257,
            "unit": "iter/sec",
            "range": "stddev: 0.00028006947821929617",
            "extra": "mean: 1.0934327345512143 msec\nrounds: 712"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_argus_model_instantiation",
            "value": 24161.197158128834,
            "unit": "iter/sec",
            "range": "stddev: 0.00002532397004544",
            "extra": "mean: 41.38867761623137 usec\nrounds: 9650"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 40151.52493845865,
            "unit": "iter/sec",
            "range": "stddev: 0.000002032845210558377",
            "extra": "mean: 24.90565430659801 usec\nrounds: 14860"
          },
          {
            "name": "benchmarks/bench_batch.py::test_cqlengine_batch_insert_10",
            "value": 658.7462578504986,
            "unit": "iter/sec",
            "range": "stddev: 0.00010684013693431544",
            "extra": "mean: 1.5180351889406078 msec\nrounds: 434"
          },
          {
            "name": "benchmarks/bench_batch.py::test_coodie_batch_insert_10",
            "value": 1467.208252206028,
            "unit": "iter/sec",
            "range": "stddev: 0.00017255434879290445",
            "extra": "mean: 681.5665046161275 usec\nrounds: 650"
          },
          {
            "name": "benchmarks/bench_batch.py::test_cqlengine_batch_insert_100",
            "value": 19.5690344612291,
            "unit": "iter/sec",
            "range": "stddev: 0.0004963508497141046",
            "extra": "mean: 51.10114154999508 msec\nrounds: 20"
          },
          {
            "name": "benchmarks/bench_batch.py::test_coodie_batch_insert_100",
            "value": 405.56061744833687,
            "unit": "iter/sec",
            "range": "stddev: 0.0004094475732766722",
            "extra": "mean: 2.465722649037507 msec\nrounds: 208"
          },
          {
            "name": "benchmarks/bench_collections.py::test_cqlengine_collection_write",
            "value": 1551.4333504240126,
            "unit": "iter/sec",
            "range": "stddev: 0.00006817286156058652",
            "extra": "mean: 644.5652336445496 usec\nrounds: 749"
          },
          {
            "name": "benchmarks/bench_collections.py::test_coodie_collection_write",
            "value": 2052.1377114601346,
            "unit": "iter/sec",
            "range": "stddev: 0.00002268880921529607",
            "extra": "mean: 487.29673180094784 usec\nrounds: 783"
          },
          {
            "name": "benchmarks/bench_collections.py::test_cqlengine_collection_read",
            "value": 1520.9806478290784,
            "unit": "iter/sec",
            "range": "stddev: 0.00007143201899835774",
            "extra": "mean: 657.4705611325937 usec\nrounds: 777"
          },
          {
            "name": "benchmarks/bench_collections.py::test_coodie_collection_read",
            "value": 2104.612404394131,
            "unit": "iter/sec",
            "range": "stddev: 0.000020169029472875034",
            "extra": "mean: 475.14687165776587 usec\nrounds: 748"
          },
          {
            "name": "benchmarks/bench_collections.py::test_cqlengine_collection_roundtrip",
            "value": 732.638621790874,
            "unit": "iter/sec",
            "range": "stddev: 0.000135453201020632",
            "extra": "mean: 1.3649294075646508 msec\nrounds: 476"
          },
          {
            "name": "benchmarks/bench_collections.py::test_coodie_collection_roundtrip",
            "value": 1038.601771056622,
            "unit": "iter/sec",
            "range": "stddev: 0.00003590599803306302",
            "extra": "mean: 962.8329431622763 usec\nrounds: 651"
          },
          {
            "name": "benchmarks/bench_delete.py::test_cqlengine_single_delete",
            "value": 894.8008783789776,
            "unit": "iter/sec",
            "range": "stddev: 0.0001233272245568591",
            "extra": "mean: 1.117567074600554 msec\nrounds: 563"
          },
          {
            "name": "benchmarks/bench_delete.py::test_coodie_single_delete",
            "value": 1043.1878963988643,
            "unit": "iter/sec",
            "range": "stddev: 0.00003460535480213812",
            "extra": "mean: 958.6000790960564 usec\nrounds: 531"
          },
          {
            "name": "benchmarks/bench_delete.py::test_cqlengine_bulk_delete",
            "value": 861.3983343350098,
            "unit": "iter/sec",
            "range": "stddev: 0.0001058969312704635",
            "extra": "mean: 1.1609031038723672 msec\nrounds: 568"
          },
          {
            "name": "benchmarks/bench_delete.py::test_coodie_bulk_delete",
            "value": 1036.3883751410935,
            "unit": "iter/sec",
            "range": "stddev: 0.000038453918004403925",
            "extra": "mean: 964.8892480715642 usec\nrounds: 778"
          },
          {
            "name": "benchmarks/bench_insert.py::test_cqlengine_single_insert",
            "value": 1608.6010936411335,
            "unit": "iter/sec",
            "range": "stddev: 0.00006844803108188539",
            "extra": "mean: 621.6581624574552 usec\nrounds: 911"
          },
          {
            "name": "benchmarks/bench_insert.py::test_coodie_single_insert",
            "value": 2080.0613729839606,
            "unit": "iter/sec",
            "range": "stddev: 0.000021463582177113556",
            "extra": "mean: 480.7550454943769 usec\nrounds: 1165"
          },
          {
            "name": "benchmarks/bench_insert.py::test_cqlengine_insert_if_not_exists",
            "value": 797.1328846451839,
            "unit": "iter/sec",
            "range": "stddev: 0.00012109183463695297",
            "extra": "mean: 1.254495980861604 msec\nrounds: 418"
          },
          {
            "name": "benchmarks/bench_insert.py::test_coodie_insert_if_not_exists",
            "value": 996.4386667690178,
            "unit": "iter/sec",
            "range": "stddev: 0.00009257391145228678",
            "extra": "mean: 1.0035740616555258 msec\nrounds: 519"
          },
          {
            "name": "benchmarks/bench_insert.py::test_cqlengine_insert_with_ttl",
            "value": 1564.2726298165085,
            "unit": "iter/sec",
            "range": "stddev: 0.00015646273626951308",
            "extra": "mean: 639.2747536069218 usec\nrounds: 901"
          },
          {
            "name": "benchmarks/bench_insert.py::test_coodie_insert_with_ttl",
            "value": 2026.2681375313196,
            "unit": "iter/sec",
            "range": "stddev: 0.00002792685396418161",
            "extra": "mean: 493.51809934609076 usec\nrounds: 765"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_get_by_pk",
            "value": 1491.8343546356923,
            "unit": "iter/sec",
            "range": "stddev: 0.00007976642172999674",
            "extra": "mean: 670.3157068964276 usec\nrounds: 754"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_get_by_pk",
            "value": 2055.4408952516546,
            "unit": "iter/sec",
            "range": "stddev: 0.000022868311742502406",
            "extra": "mean: 486.51362455137223 usec\nrounds: 1116"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_filter_secondary_index",
            "value": 211.99703992720615,
            "unit": "iter/sec",
            "range": "stddev: 0.0021166917633847907",
            "extra": "mean: 4.717046994351299 msec\nrounds: 177"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_filter_secondary_index",
            "value": 513.0613613016843,
            "unit": "iter/sec",
            "range": "stddev: 0.00010674671376084884",
            "extra": "mean: 1.9490846035704326 msec\nrounds: 280"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_filter_limit",
            "value": 879.8767915451973,
            "unit": "iter/sec",
            "range": "stddev: 0.00014267733275748312",
            "extra": "mean: 1.1365227604695063 msec\nrounds: 597"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_filter_limit",
            "value": 1475.2283092818102,
            "unit": "iter/sec",
            "range": "stddev: 0.00007667413382782701",
            "extra": "mean: 677.8611783059077 usec\nrounds: 673"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_count",
            "value": 921.4142087359185,
            "unit": "iter/sec",
            "range": "stddev: 0.00008628425937510747",
            "extra": "mean: 1.0852882346712376 msec\nrounds: 473"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_count",
            "value": 1064.6914576049016,
            "unit": "iter/sec",
            "range": "stddev: 0.00005961943774588197",
            "extra": "mean: 939.239244249757 usec\nrounds: 565"
          },
          {
            "name": "benchmarks/bench_schema.py::test_cqlengine_sync_table_create",
            "value": 7244.1759508268815,
            "unit": "iter/sec",
            "range": "stddev: 0.00006404741874275518",
            "extra": "mean: 138.04192592614424 usec\nrounds: 135"
          },
          {
            "name": "benchmarks/bench_schema.py::test_coodie_sync_table_create",
            "value": 38120.4508945491,
            "unit": "iter/sec",
            "range": "stddev: 0.000006177082690711601",
            "extra": "mean: 26.232638296075127 usec\nrounds: 141"
          },
          {
            "name": "benchmarks/bench_schema.py::test_cqlengine_sync_table_noop",
            "value": 5986.492506653926,
            "unit": "iter/sec",
            "range": "stddev: 0.00006579059665443444",
            "extra": "mean: 167.0427214079881 usec\nrounds: 2046"
          },
          {
            "name": "benchmarks/bench_schema.py::test_coodie_sync_table_noop",
            "value": 56997.27612621538,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025143822400273947",
            "extra": "mean: 17.544698062159835 usec\nrounds: 8929"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_cqlengine_model_instantiation",
            "value": 72300.33881084192,
            "unit": "iter/sec",
            "range": "stddev: 0.000019824548383442743",
            "extra": "mean: 13.831193829067415 usec\nrounds: 15070"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 473999.7946787681,
            "unit": "iter/sec",
            "range": "stddev: 4.840121834594114e-7",
            "extra": "mean: 2.1097055552053665 usec\nrounds: 33986"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_cqlengine_model_serialization",
            "value": 214015.4415991567,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010525296782458964",
            "extra": "mean: 4.672560038321741 usec\nrounds: 41815"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 507398.15901900775,
            "unit": "iter/sec",
            "range": "stddev: 6.946296540124928e-7",
            "extra": "mean: 1.9708388416965834 usec\nrounds: 50894"
          },
          {
            "name": "benchmarks/bench_update.py::test_cqlengine_partial_update",
            "value": 1870.3666973597271,
            "unit": "iter/sec",
            "range": "stddev: 0.00008022330102520365",
            "extra": "mean: 534.6545152945857 usec\nrounds: 850"
          },
          {
            "name": "benchmarks/bench_update.py::test_coodie_partial_update",
            "value": 1043.6588855653538,
            "unit": "iter/sec",
            "range": "stddev: 0.00006322744806778669",
            "extra": "mean: 958.1674758207002 usec\nrounds: 517"
          },
          {
            "name": "benchmarks/bench_update.py::test_cqlengine_update_if_condition",
            "value": 836.167228431765,
            "unit": "iter/sec",
            "range": "stddev: 0.00013137200167164575",
            "extra": "mean: 1.1959330215266915 msec\nrounds: 511"
          },
          {
            "name": "benchmarks/bench_update.py::test_coodie_update_if_condition",
            "value": 686.0541074767027,
            "unit": "iter/sec",
            "range": "stddev: 0.00010206579563670663",
            "extra": "mean: 1.4576109800989105 msec\nrounds: 402"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "aee9586bc2c4db392df5a9d9bb7b4ecb2365e4b4",
          "message": "fix(ci): replace deprecated `gh copilot suggest` with new Copilot CLI (`copilot -p`)\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-02-25T21:37:43+02:00",
          "tree_id": "c28b85e8dba671af8bdb421838cb4bc198d76077",
          "url": "https://github.com/fruch/coodie/commit/aee9586bc2c4db392df5a9d9bb7b4ecb2365e4b4"
        },
        "date": 1772048338732,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_get_or_create_user",
            "value": 1372.1596904453438,
            "unit": "iter/sec",
            "range": "stddev: 0.00010668742168492552",
            "extra": "mean: 728.7781494845132 usec\nrounds: 582"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_get_or_create_user",
            "value": 2053.0134419433416,
            "unit": "iter/sec",
            "range": "stddev: 0.000040477254568267906",
            "extra": "mean: 487.0888712026259 usec\nrounds: 823"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_filter_runs_by_status",
            "value": 836.7073523552829,
            "unit": "iter/sec",
            "range": "stddev: 0.0007588858442562368",
            "extra": "mean: 1.1951610048424433 msec\nrounds: 826"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_filter_runs_by_status",
            "value": 2013.7570673588239,
            "unit": "iter/sec",
            "range": "stddev: 0.00005696434142157429",
            "extra": "mean: 496.5842286585077 usec\nrounds: 984"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_latest_runs",
            "value": 1038.2904291412224,
            "unit": "iter/sec",
            "range": "stddev: 0.00008894314054893313",
            "extra": "mean: 963.121658385224 usec\nrounds: 644"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_latest_runs",
            "value": 2002.9492090428748,
            "unit": "iter/sec",
            "range": "stddev: 0.00003782789061920313",
            "extra": "mean: 499.2637833676561 usec\nrounds: 974"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_list_mutation",
            "value": 1302.6487619128457,
            "unit": "iter/sec",
            "range": "stddev: 0.00009833282649456823",
            "extra": "mean: 767.6666414142 usec\nrounds: 594"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_list_mutation",
            "value": 1018.1769017299478,
            "unit": "iter/sec",
            "range": "stddev: 0.00003172765957680164",
            "extra": "mean: 982.1475995978066 usec\nrounds: 994"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_batch_events",
            "value": 318.49965146583935,
            "unit": "iter/sec",
            "range": "stddev: 0.00015812251691609003",
            "extra": "mean: 3.1397208612244114 msec\nrounds: 245"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_batch_events",
            "value": 811.0179676116924,
            "unit": "iter/sec",
            "range": "stddev: 0.00009486822176206135",
            "extra": "mean: 1.2330183053093473 msec\nrounds: 452"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_notification_feed",
            "value": 705.6897087021597,
            "unit": "iter/sec",
            "range": "stddev: 0.0001400486892531428",
            "extra": "mean: 1.4170533984959324 msec\nrounds: 665"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_notification_feed",
            "value": 1399.0367835777363,
            "unit": "iter/sec",
            "range": "stddev: 0.00003360542043801729",
            "extra": "mean: 714.777489583022 usec\nrounds: 768"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_status_update",
            "value": 1114.6014607959262,
            "unit": "iter/sec",
            "range": "stddev: 0.00009355120897243227",
            "extra": "mean: 897.1816700167517 usec\nrounds: 597"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_status_update",
            "value": 1030.3581412127614,
            "unit": "iter/sec",
            "range": "stddev: 0.00004598767635917869",
            "extra": "mean: 970.5363213056879 usec\nrounds: 582"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_comment_with_collections",
            "value": 1270.3447356646625,
            "unit": "iter/sec",
            "range": "stddev: 0.00007830820406739788",
            "extra": "mean: 787.1878962656431 usec\nrounds: 723"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_comment_with_collections",
            "value": 2018.8464914373326,
            "unit": "iter/sec",
            "range": "stddev: 0.00003902956753560999",
            "extra": "mean: 495.33236144569 usec\nrounds: 747"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_multi_model_lookup",
            "value": 680.0228292137359,
            "unit": "iter/sec",
            "range": "stddev: 0.00015232940559881602",
            "extra": "mean: 1.4705388658145961 msec\nrounds: 626"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_multi_model_lookup",
            "value": 1022.6983526351534,
            "unit": "iter/sec",
            "range": "stddev: 0.000029984849087852426",
            "extra": "mean: 977.8054275958624 usec\nrounds: 732"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_argus_model_instantiation",
            "value": 27194.932474153546,
            "unit": "iter/sec",
            "range": "stddev: 0.00002548594637317992",
            "extra": "mean: 36.77155664756346 usec\nrounds: 11192"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 46734.760705889064,
            "unit": "iter/sec",
            "range": "stddev: 0.000001915048237709547",
            "extra": "mean: 21.39734931549547 usec\nrounds: 17311"
          },
          {
            "name": "benchmarks/bench_batch.py::test_cqlengine_batch_insert_10",
            "value": 558.8409374186361,
            "unit": "iter/sec",
            "range": "stddev: 0.00011716982993314294",
            "extra": "mean: 1.78941794174768 msec\nrounds: 412"
          },
          {
            "name": "benchmarks/bench_batch.py::test_coodie_batch_insert_10",
            "value": 1328.5570828304067,
            "unit": "iter/sec",
            "range": "stddev: 0.00013190866017277796",
            "extra": "mean: 752.6962995594915 usec\nrounds: 681"
          },
          {
            "name": "benchmarks/bench_batch.py::test_cqlengine_batch_insert_100",
            "value": 18.45390063861386,
            "unit": "iter/sec",
            "range": "stddev: 0.0004017430247259929",
            "extra": "mean: 54.18908552631688 msec\nrounds: 19"
          },
          {
            "name": "benchmarks/bench_batch.py::test_coodie_batch_insert_100",
            "value": 416.1908865943804,
            "unit": "iter/sec",
            "range": "stddev: 0.00024819860535864796",
            "extra": "mean: 2.4027436260866515 msec\nrounds: 230"
          },
          {
            "name": "benchmarks/bench_collections.py::test_cqlengine_collection_write",
            "value": 1525.6569127911023,
            "unit": "iter/sec",
            "range": "stddev: 0.00006727109441098325",
            "extra": "mean: 655.4553593380028 usec\nrounds: 846"
          },
          {
            "name": "benchmarks/bench_collections.py::test_coodie_collection_write",
            "value": 2033.5969757846526,
            "unit": "iter/sec",
            "range": "stddev: 0.00004651644339260158",
            "extra": "mean: 491.7395196332624 usec\nrounds: 764"
          },
          {
            "name": "benchmarks/bench_collections.py::test_cqlengine_collection_read",
            "value": 1426.0225467961563,
            "unit": "iter/sec",
            "range": "stddev: 0.00008958420967295353",
            "extra": "mean: 701.2511844547614 usec\nrounds: 862"
          },
          {
            "name": "benchmarks/bench_collections.py::test_coodie_collection_read",
            "value": 2034.4284698319884,
            "unit": "iter/sec",
            "range": "stddev: 0.000024459989258337337",
            "extra": "mean: 491.538540100446 usec\nrounds: 798"
          },
          {
            "name": "benchmarks/bench_collections.py::test_cqlengine_collection_roundtrip",
            "value": 641.5202902224399,
            "unit": "iter/sec",
            "range": "stddev: 0.0004235879398897685",
            "extra": "mean: 1.5587971498972564 msec\nrounds: 487"
          },
          {
            "name": "benchmarks/bench_collections.py::test_coodie_collection_roundtrip",
            "value": 1019.4124350396104,
            "unit": "iter/sec",
            "range": "stddev: 0.00003204682415374569",
            "extra": "mean: 980.9572314675012 usec\nrounds: 661"
          },
          {
            "name": "benchmarks/bench_delete.py::test_cqlengine_single_delete",
            "value": 887.1198260307323,
            "unit": "iter/sec",
            "range": "stddev: 0.00010490028702291817",
            "extra": "mean: 1.1272434350546883 msec\nrounds: 639"
          },
          {
            "name": "benchmarks/bench_delete.py::test_coodie_single_delete",
            "value": 1023.3888697862723,
            "unit": "iter/sec",
            "range": "stddev: 0.00003104029207264547",
            "extra": "mean: 977.1456672270074 usec\nrounds: 595"
          },
          {
            "name": "benchmarks/bench_delete.py::test_cqlengine_bulk_delete",
            "value": 809.3843361569916,
            "unit": "iter/sec",
            "range": "stddev: 0.00011281310639463802",
            "extra": "mean: 1.2355069839231925 msec\nrounds: 622"
          },
          {
            "name": "benchmarks/bench_delete.py::test_coodie_bulk_delete",
            "value": 1020.7951956869149,
            "unit": "iter/sec",
            "range": "stddev: 0.00002995325347457437",
            "extra": "mean: 979.6284349938369 usec\nrounds: 823"
          },
          {
            "name": "benchmarks/bench_insert.py::test_cqlengine_single_insert",
            "value": 1591.3035966067205,
            "unit": "iter/sec",
            "range": "stddev: 0.00007111382083857079",
            "extra": "mean: 628.4155972074655 usec\nrounds: 931"
          },
          {
            "name": "benchmarks/bench_insert.py::test_coodie_single_insert",
            "value": 2042.939741604227,
            "unit": "iter/sec",
            "range": "stddev: 0.000019342770230031172",
            "extra": "mean: 489.4906979560473 usec\nrounds: 1321"
          },
          {
            "name": "benchmarks/bench_insert.py::test_cqlengine_insert_if_not_exists",
            "value": 690.1901405424125,
            "unit": "iter/sec",
            "range": "stddev: 0.00036116341417042475",
            "extra": "mean: 1.448876101322038 msec\nrounds: 454"
          },
          {
            "name": "benchmarks/bench_insert.py::test_coodie_insert_if_not_exists",
            "value": 813.6290150128992,
            "unit": "iter/sec",
            "range": "stddev: 0.0003339561290482866",
            "extra": "mean: 1.2290613800002523 msec\nrounds: 450"
          },
          {
            "name": "benchmarks/bench_insert.py::test_cqlengine_insert_with_ttl",
            "value": 1581.1965856370675,
            "unit": "iter/sec",
            "range": "stddev: 0.00006688804917602468",
            "extra": "mean: 632.4324306563676 usec\nrounds: 959"
          },
          {
            "name": "benchmarks/bench_insert.py::test_coodie_insert_with_ttl",
            "value": 2063.334474361722,
            "unit": "iter/sec",
            "range": "stddev: 0.000020931996183511495",
            "extra": "mean: 484.6523975756974 usec\nrounds: 825"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_get_by_pk",
            "value": 1495.677039311886,
            "unit": "iter/sec",
            "range": "stddev: 0.00007335474538664581",
            "extra": "mean: 668.5935357141464 usec\nrounds: 812"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_get_by_pk",
            "value": 2008.4522532652138,
            "unit": "iter/sec",
            "range": "stddev: 0.00009310761379312788",
            "extra": "mean: 497.89582917605514 usec\nrounds: 1323"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_filter_secondary_index",
            "value": 205.65220950765485,
            "unit": "iter/sec",
            "range": "stddev: 0.0008078163432107983",
            "extra": "mean: 4.86257843956098 msec\nrounds: 182"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_filter_secondary_index",
            "value": 537.286011509744,
            "unit": "iter/sec",
            "range": "stddev: 0.000041524223131248156",
            "extra": "mean: 1.861206096153621 msec\nrounds: 364"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_filter_limit",
            "value": 831.2772670679144,
            "unit": "iter/sec",
            "range": "stddev: 0.00016386201871311916",
            "extra": "mean: 1.2029680584520317 msec\nrounds: 633"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_filter_limit",
            "value": 1390.9930833941523,
            "unit": "iter/sec",
            "range": "stddev: 0.000028190022697300205",
            "extra": "mean: 718.910835674256 usec\nrounds: 712"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_count",
            "value": 947.9549591683784,
            "unit": "iter/sec",
            "range": "stddev: 0.0000669227296269677",
            "extra": "mean: 1.054902440594097 msec\nrounds: 606"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_count",
            "value": 1046.9513666817,
            "unit": "iter/sec",
            "range": "stddev: 0.00006016853127222843",
            "extra": "mean: 955.1542046976722 usec\nrounds: 596"
          },
          {
            "name": "benchmarks/bench_schema.py::test_cqlengine_sync_table_create",
            "value": 3662.5591861715584,
            "unit": "iter/sec",
            "range": "stddev: 0.000069920649986849",
            "extra": "mean: 273.0331304339388 usec\nrounds: 92"
          },
          {
            "name": "benchmarks/bench_schema.py::test_coodie_sync_table_create",
            "value": 31569.44510090989,
            "unit": "iter/sec",
            "range": "stddev: 0.000010905017302509983",
            "extra": "mean: 31.676198197451946 usec\nrounds: 111"
          },
          {
            "name": "benchmarks/bench_schema.py::test_cqlengine_sync_table_noop",
            "value": 4562.733143091229,
            "unit": "iter/sec",
            "range": "stddev: 0.000063951142648326",
            "extra": "mean: 219.16688279571505 usec\nrounds: 1860"
          },
          {
            "name": "benchmarks/bench_schema.py::test_coodie_sync_table_noop",
            "value": 48791.3692281844,
            "unit": "iter/sec",
            "range": "stddev: 0.000007908612412769647",
            "extra": "mean: 20.495428101705098 usec\nrounds: 9124"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_cqlengine_model_instantiation",
            "value": 83161.61519527003,
            "unit": "iter/sec",
            "range": "stddev: 0.00001728223718185932",
            "extra": "mean: 12.024778470835628 usec\nrounds: 22286"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 481995.2215633491,
            "unit": "iter/sec",
            "range": "stddev: 4.54956309224901e-7",
            "extra": "mean: 2.074709364869853 usec\nrounds: 37566"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_cqlengine_model_serialization",
            "value": 215596.23170722253,
            "unit": "iter/sec",
            "range": "stddev: 6.838536795522361e-7",
            "extra": "mean: 4.638299992914485 usec\nrounds: 42081"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 511082.40438546625,
            "unit": "iter/sec",
            "range": "stddev: 4.4097837842395377e-7",
            "extra": "mean: 1.9566316339972927 usec\nrounds: 54511"
          },
          {
            "name": "benchmarks/bench_update.py::test_cqlengine_partial_update",
            "value": 1795.8522918888136,
            "unit": "iter/sec",
            "range": "stddev: 0.00007121061737795619",
            "extra": "mean: 556.8386690356564 usec\nrounds: 985"
          },
          {
            "name": "benchmarks/bench_update.py::test_coodie_partial_update",
            "value": 1031.8882353809315,
            "unit": "iter/sec",
            "range": "stddev: 0.000032126934830147175",
            "extra": "mean: 969.0972003676738 usec\nrounds: 544"
          },
          {
            "name": "benchmarks/bench_update.py::test_cqlengine_update_if_condition",
            "value": 703.1529040360834,
            "unit": "iter/sec",
            "range": "stddev: 0.00039133385884789",
            "extra": "mean: 1.422165782520445 msec\nrounds: 492"
          },
          {
            "name": "benchmarks/bench_update.py::test_coodie_update_if_condition",
            "value": 579.1757649300472,
            "unit": "iter/sec",
            "range": "stddev: 0.0005601086712425317",
            "extra": "mean: 1.726591581608702 msec\nrounds: 435"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "971b44370e2558b462b3f086bb5c6f1ef4fd207c",
          "message": "fix(ci): use saved SHA to restore detached HEAD after gh-pages bootstrap\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-02-25T21:39:38+02:00",
          "tree_id": "05af536a7968e84abc501041233e490440471a7f",
          "url": "https://github.com/fruch/coodie/commit/971b44370e2558b462b3f086bb5c6f1ef4fd207c"
        },
        "date": 1772048446201,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_get_or_create_user",
            "value": 1517.513729142307,
            "unit": "iter/sec",
            "range": "stddev: 0.0001837605782101156",
            "extra": "mean: 658.9726213318652 usec\nrounds: 375"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_get_or_create_user",
            "value": 2175.5971162548412,
            "unit": "iter/sec",
            "range": "stddev: 0.00005375506241554137",
            "extra": "mean: 459.64392604152715 usec\nrounds: 960"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_filter_runs_by_status",
            "value": 1067.1111264190124,
            "unit": "iter/sec",
            "range": "stddev: 0.0001508581461883116",
            "extra": "mean: 937.1095242496228 usec\nrounds: 866"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_filter_runs_by_status",
            "value": 2177.3020614635816,
            "unit": "iter/sec",
            "range": "stddev: 0.000034640335374187196",
            "extra": "mean: 459.2840000012678 usec\nrounds: 1027"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_latest_runs",
            "value": 993.4874271454638,
            "unit": "iter/sec",
            "range": "stddev: 0.0011694705596961054",
            "extra": "mean: 1.0065552644921218 msec\nrounds: 828"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_latest_runs",
            "value": 2089.8942798634807,
            "unit": "iter/sec",
            "range": "stddev: 0.0001032819150418423",
            "extra": "mean: 478.4931035197261 usec\nrounds: 966"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_list_mutation",
            "value": 1380.856472234345,
            "unit": "iter/sec",
            "range": "stddev: 0.00008871176131728174",
            "extra": "mean: 724.1882267328723 usec\nrounds: 591"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_list_mutation",
            "value": 1064.3501858976654,
            "unit": "iter/sec",
            "range": "stddev: 0.00007743538686458269",
            "extra": "mean: 939.5404005652586 usec\nrounds: 1061"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_batch_events",
            "value": 355.3901323167226,
            "unit": "iter/sec",
            "range": "stddev: 0.00017032543502627732",
            "extra": "mean: 2.813809132744302 msec\nrounds: 226"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_batch_events",
            "value": 864.3369834944561,
            "unit": "iter/sec",
            "range": "stddev: 0.00010682279008155185",
            "extra": "mean: 1.1569561630431078 msec\nrounds: 460"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_notification_feed",
            "value": 796.0351837700151,
            "unit": "iter/sec",
            "range": "stddev: 0.00011892512299321828",
            "extra": "mean: 1.2562258809516553 msec\nrounds: 714"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_notification_feed",
            "value": 1934.5098939833254,
            "unit": "iter/sec",
            "range": "stddev: 0.00009193296882875131",
            "extra": "mean: 516.9267953139864 usec\nrounds: 811"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_status_update",
            "value": 1257.6524101989526,
            "unit": "iter/sec",
            "range": "stddev: 0.00008659519084581892",
            "extra": "mean: 795.1322574429022 usec\nrounds: 571"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_status_update",
            "value": 1103.7376984764865,
            "unit": "iter/sec",
            "range": "stddev: 0.000032945506354170545",
            "extra": "mean: 906.0123627020461 usec\nrounds: 681"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_comment_with_collections",
            "value": 1355.384285503374,
            "unit": "iter/sec",
            "range": "stddev: 0.00008832320048136502",
            "extra": "mean: 737.7981364367166 usec\nrounds: 623"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_comment_with_collections",
            "value": 2140.8473939795135,
            "unit": "iter/sec",
            "range": "stddev: 0.00003811890468745008",
            "extra": "mean: 467.1047561877591 usec\nrounds: 808"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_multi_model_lookup",
            "value": 762.4729311401786,
            "unit": "iter/sec",
            "range": "stddev: 0.00011309523828923779",
            "extra": "mean: 1.311521969054863 msec\nrounds: 614"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_multi_model_lookup",
            "value": 1088.367615538935,
            "unit": "iter/sec",
            "range": "stddev: 0.0002507336107058853",
            "extra": "mean: 918.8071987099896 usec\nrounds: 775"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_argus_model_instantiation",
            "value": 34987.44706400241,
            "unit": "iter/sec",
            "range": "stddev: 0.00002208319384683751",
            "extra": "mean: 28.5816795426858 usec\nrounds: 12504"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 66128.20992754954,
            "unit": "iter/sec",
            "range": "stddev: 0.000001033454228932858",
            "extra": "mean: 15.122139266972537 usec\nrounds: 18224"
          },
          {
            "name": "benchmarks/bench_batch.py::test_cqlengine_batch_insert_10",
            "value": 655.0538124449929,
            "unit": "iter/sec",
            "range": "stddev: 0.00011654657178821457",
            "extra": "mean: 1.5265921379306122 msec\nrounds: 464"
          },
          {
            "name": "benchmarks/bench_batch.py::test_coodie_batch_insert_10",
            "value": 1881.7465224605726,
            "unit": "iter/sec",
            "range": "stddev: 0.0001699306825607245",
            "extra": "mean: 531.4212026242511 usec\nrounds: 686"
          },
          {
            "name": "benchmarks/bench_batch.py::test_cqlengine_batch_insert_100",
            "value": 19.024166684303722,
            "unit": "iter/sec",
            "range": "stddev: 0.0008398296936732512",
            "extra": "mean: 52.56472026315195 msec\nrounds: 19"
          },
          {
            "name": "benchmarks/bench_batch.py::test_coodie_batch_insert_100",
            "value": 450.6867177023662,
            "unit": "iter/sec",
            "range": "stddev: 0.0004002129542382007",
            "extra": "mean: 2.218836190909004 msec\nrounds: 220"
          },
          {
            "name": "benchmarks/bench_collections.py::test_cqlengine_collection_write",
            "value": 1539.8511223602213,
            "unit": "iter/sec",
            "range": "stddev: 0.00007633662544934262",
            "extra": "mean: 649.4134306096037 usec\nrounds: 771"
          },
          {
            "name": "benchmarks/bench_collections.py::test_coodie_collection_write",
            "value": 2124.1283363662055,
            "unit": "iter/sec",
            "range": "stddev: 0.000022816163168652743",
            "extra": "mean: 470.78134728465733 usec\nrounds: 884"
          },
          {
            "name": "benchmarks/bench_collections.py::test_cqlengine_collection_read",
            "value": 1520.7890139304916,
            "unit": "iter/sec",
            "range": "stddev: 0.0000797410375785849",
            "extra": "mean: 657.5534086845432 usec\nrounds: 783"
          },
          {
            "name": "benchmarks/bench_collections.py::test_coodie_collection_read",
            "value": 2234.8479497533467,
            "unit": "iter/sec",
            "range": "stddev: 0.00001686008595276476",
            "extra": "mean: 447.45773425452364 usec\nrounds: 651"
          },
          {
            "name": "benchmarks/bench_collections.py::test_cqlengine_collection_roundtrip",
            "value": 719.4728988952259,
            "unit": "iter/sec",
            "range": "stddev: 0.00013898040341743588",
            "extra": "mean: 1.389906418345337 msec\nrounds: 447"
          },
          {
            "name": "benchmarks/bench_collections.py::test_coodie_collection_roundtrip",
            "value": 1065.5121660531186,
            "unit": "iter/sec",
            "range": "stddev: 0.00007127188072475523",
            "extra": "mean: 938.5157972472624 usec\nrounds: 799"
          },
          {
            "name": "benchmarks/bench_delete.py::test_cqlengine_single_delete",
            "value": 944.2799586107361,
            "unit": "iter/sec",
            "range": "stddev: 0.00010293343067135291",
            "extra": "mean: 1.0590079677972213 msec\nrounds: 590"
          },
          {
            "name": "benchmarks/bench_delete.py::test_coodie_single_delete",
            "value": 1069.9676104543119,
            "unit": "iter/sec",
            "range": "stddev: 0.00003114374945750204",
            "extra": "mean: 934.6077303923215 usec\nrounds: 612"
          },
          {
            "name": "benchmarks/bench_delete.py::test_cqlengine_bulk_delete",
            "value": 900.3895453651068,
            "unit": "iter/sec",
            "range": "stddev: 0.00010371056321139093",
            "extra": "mean: 1.110630398973037 msec\nrounds: 584"
          },
          {
            "name": "benchmarks/bench_delete.py::test_coodie_bulk_delete",
            "value": 1067.0085948207484,
            "unit": "iter/sec",
            "range": "stddev: 0.000022137020335954842",
            "extra": "mean: 937.1995735123338 usec\nrounds: 823"
          },
          {
            "name": "benchmarks/bench_insert.py::test_cqlengine_single_insert",
            "value": 1684.6065734146405,
            "unit": "iter/sec",
            "range": "stddev: 0.00006721780542667916",
            "extra": "mean: 593.6104107518908 usec\nrounds: 930"
          },
          {
            "name": "benchmarks/bench_insert.py::test_coodie_single_insert",
            "value": 2119.9239536674627,
            "unit": "iter/sec",
            "range": "stddev: 0.000023574758978250336",
            "extra": "mean: 471.71503405582195 usec\nrounds: 1292"
          },
          {
            "name": "benchmarks/bench_insert.py::test_cqlengine_insert_if_not_exists",
            "value": 809.1452851455975,
            "unit": "iter/sec",
            "range": "stddev: 0.00011889038651740758",
            "extra": "mean: 1.2358719977217194 msec\nrounds: 439"
          },
          {
            "name": "benchmarks/bench_insert.py::test_coodie_insert_if_not_exists",
            "value": 1044.5586686403492,
            "unit": "iter/sec",
            "range": "stddev: 0.0003786129793945504",
            "extra": "mean: 957.3421101388694 usec\nrounds: 572"
          },
          {
            "name": "benchmarks/bench_insert.py::test_cqlengine_insert_with_ttl",
            "value": 1666.396907375214,
            "unit": "iter/sec",
            "range": "stddev: 0.00007282967940398933",
            "extra": "mean: 600.0971290658038 usec\nrounds: 953"
          },
          {
            "name": "benchmarks/bench_insert.py::test_coodie_insert_with_ttl",
            "value": 2159.2740979379623,
            "unit": "iter/sec",
            "range": "stddev: 0.000024441121242497052",
            "extra": "mean: 463.1186012720516 usec\nrounds: 785"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_get_by_pk",
            "value": 1592.4800660245792,
            "unit": "iter/sec",
            "range": "stddev: 0.00007436731515096622",
            "extra": "mean: 627.9513454107912 usec\nrounds: 828"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_get_by_pk",
            "value": 2204.2600244978703,
            "unit": "iter/sec",
            "range": "stddev: 0.00002163358504685498",
            "extra": "mean: 453.66698524045484 usec\nrounds: 1355"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_filter_secondary_index",
            "value": 242.49218762548318,
            "unit": "iter/sec",
            "range": "stddev: 0.0005993276633934469",
            "extra": "mean: 4.123844193877491 msec\nrounds: 196"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_filter_secondary_index",
            "value": 559.4300493259113,
            "unit": "iter/sec",
            "range": "stddev: 0.000048057874936357804",
            "extra": "mean: 1.7875335820894072 msec\nrounds: 335"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_filter_limit",
            "value": 879.71694420968,
            "unit": "iter/sec",
            "range": "stddev: 0.00014251516789381863",
            "extra": "mean: 1.1367292702295053 msec\nrounds: 655"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_filter_limit",
            "value": 1933.809625098458,
            "unit": "iter/sec",
            "range": "stddev: 0.00009783966040627216",
            "extra": "mean: 517.1139842419008 usec\nrounds: 698"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_count",
            "value": 1022.2232798825471,
            "unit": "iter/sec",
            "range": "stddev: 0.00006688685883306549",
            "extra": "mean: 978.2598573913317 usec\nrounds: 575"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_count",
            "value": 1103.855174542951,
            "unit": "iter/sec",
            "range": "stddev: 0.00006816185734713637",
            "extra": "mean: 905.9159417484707 usec\nrounds: 618"
          },
          {
            "name": "benchmarks/bench_schema.py::test_cqlengine_sync_table_create",
            "value": 6677.499363687949,
            "unit": "iter/sec",
            "range": "stddev: 0.00005828135088178254",
            "extra": "mean: 149.75665972174724 usec\nrounds: 144"
          },
          {
            "name": "benchmarks/bench_schema.py::test_coodie_sync_table_create",
            "value": 59234.80479747743,
            "unit": "iter/sec",
            "range": "stddev: 0.0000052492188374799705",
            "extra": "mean: 16.881966665020325 usec\nrounds: 180"
          },
          {
            "name": "benchmarks/bench_schema.py::test_cqlengine_sync_table_noop",
            "value": 5188.91412073215,
            "unit": "iter/sec",
            "range": "stddev: 0.00006036286102620081",
            "extra": "mean: 192.71854895507522 usec\nrounds: 2727"
          },
          {
            "name": "benchmarks/bench_schema.py::test_coodie_sync_table_noop",
            "value": 63922.92831298926,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016153889453705596",
            "extra": "mean: 15.643839016630253 usec\nrounds: 10206"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_cqlengine_model_instantiation",
            "value": 93102.55254558605,
            "unit": "iter/sec",
            "range": "stddev: 0.000016373124962306874",
            "extra": "mean: 10.740844076325054 usec\nrounds: 21626"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 503023.9877768347,
            "unit": "iter/sec",
            "range": "stddev: 5.757467456391153e-7",
            "extra": "mean: 1.9879767651232714 usec\nrounds: 37616"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_cqlengine_model_serialization",
            "value": 229567.15006181248,
            "unit": "iter/sec",
            "range": "stddev: 7.695158286194083e-7",
            "extra": "mean: 4.356023933436223 usec\nrounds: 44791"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 567105.6112041901,
            "unit": "iter/sec",
            "range": "stddev: 5.418112330705055e-7",
            "extra": "mean: 1.7633399850807392 usec\nrounds: 53620"
          },
          {
            "name": "benchmarks/bench_update.py::test_cqlengine_partial_update",
            "value": 1970.6148937577218,
            "unit": "iter/sec",
            "range": "stddev: 0.00010097221150580745",
            "extra": "mean: 507.4558216157203 usec\nrounds: 953"
          },
          {
            "name": "benchmarks/bench_update.py::test_coodie_partial_update",
            "value": 1116.8568558369,
            "unit": "iter/sec",
            "range": "stddev: 0.000021710940172767937",
            "extra": "mean: 895.3698898599365 usec\nrounds: 572"
          },
          {
            "name": "benchmarks/bench_update.py::test_cqlengine_update_if_condition",
            "value": 892.1625519093559,
            "unit": "iter/sec",
            "range": "stddev: 0.00009981445753875127",
            "extra": "mean: 1.1208719732293813 msec\nrounds: 523"
          },
          {
            "name": "benchmarks/bench_update.py::test_coodie_update_if_condition",
            "value": 743.4127604918929,
            "unit": "iter/sec",
            "range": "stddev: 0.00006582209822623537",
            "extra": "mean: 1.3451477471792808 msec\nrounds: 443"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "5213d4350e84197a8a0c2aa7d742f2be3b464a81",
          "message": "docs(plans): add Phase 3 benchmark results from CI run #22404800091\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-02-25T21:42:06+02:00",
          "tree_id": "a8cb4316df0bd3b4d25c2a417c4c2aee19f952bc",
          "url": "https://github.com/fruch/coodie/commit/5213d4350e84197a8a0c2aa7d742f2be3b464a81"
        },
        "date": 1772048602506,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_get_or_create_user",
            "value": 1465.5389438204063,
            "unit": "iter/sec",
            "range": "stddev: 0.00007525691785053222",
            "extra": "mean: 682.342836549381 usec\nrounds: 881"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_get_or_create_user",
            "value": 2071.262123314942,
            "unit": "iter/sec",
            "range": "stddev: 0.000020333706452355534",
            "extra": "mean: 482.79741551955505 usec\nrounds: 799"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_filter_runs_by_status",
            "value": 974.4279434947813,
            "unit": "iter/sec",
            "range": "stddev: 0.0006046233941220308",
            "extra": "mean: 1.0262431477626808 msec\nrounds: 961"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_filter_runs_by_status",
            "value": 2059.0700723620153,
            "unit": "iter/sec",
            "range": "stddev: 0.000032598868153791106",
            "extra": "mean: 485.65612866825495 usec\nrounds: 886"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_latest_runs",
            "value": 1075.0630394180032,
            "unit": "iter/sec",
            "range": "stddev: 0.00007613245241632495",
            "extra": "mean: 930.1780112739814 usec\nrounds: 887"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_latest_runs",
            "value": 2077.3571292516926,
            "unit": "iter/sec",
            "range": "stddev: 0.000018998830549756147",
            "extra": "mean: 481.3808785782639 usec\nrounds: 1013"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_list_mutation",
            "value": 1360.0451688659864,
            "unit": "iter/sec",
            "range": "stddev: 0.00008157524075989384",
            "extra": "mean: 735.2696975746811 usec\nrounds: 701"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_list_mutation",
            "value": 1041.4025446912162,
            "unit": "iter/sec",
            "range": "stddev: 0.00002291513729717879",
            "extra": "mean: 960.2434765477816 usec\nrounds: 1066"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_batch_events",
            "value": 341.37737316566046,
            "unit": "iter/sec",
            "range": "stddev: 0.00014208517738508974",
            "extra": "mean: 2.929309551851081 msec\nrounds: 270"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_batch_events",
            "value": 854.0521913320563,
            "unit": "iter/sec",
            "range": "stddev: 0.00005497845816357732",
            "extra": "mean: 1.1708886296987429 msec\nrounds: 532"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_notification_feed",
            "value": 728.5871370120642,
            "unit": "iter/sec",
            "range": "stddev: 0.00010788736434190424",
            "extra": "mean: 1.3725194272588999 msec\nrounds: 653"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_notification_feed",
            "value": 1443.003564315599,
            "unit": "iter/sec",
            "range": "stddev: 0.00006461743884516814",
            "extra": "mean: 692.9989812424955 usec\nrounds: 853"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_status_update",
            "value": 1158.714365848069,
            "unit": "iter/sec",
            "range": "stddev: 0.00006469100169553006",
            "extra": "mean: 863.0254612128631 usec\nrounds: 709"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_status_update",
            "value": 1033.6350781994877,
            "unit": "iter/sec",
            "range": "stddev: 0.000024097289326898604",
            "extra": "mean: 967.4594265337074 usec\nrounds: 701"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_comment_with_collections",
            "value": 1335.7950501690038,
            "unit": "iter/sec",
            "range": "stddev: 0.00006103932699753407",
            "extra": "mean: 748.6178361519462 usec\nrounds: 946"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_comment_with_collections",
            "value": 2066.910273277988,
            "unit": "iter/sec",
            "range": "stddev: 0.000021565836717017362",
            "extra": "mean: 483.8139385770548 usec\nrounds: 928"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_multi_model_lookup",
            "value": 756.2617103466092,
            "unit": "iter/sec",
            "range": "stddev: 0.00010535008702227006",
            "extra": "mean: 1.3222935741936226 msec\nrounds: 620"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_multi_model_lookup",
            "value": 1032.631375901861,
            "unit": "iter/sec",
            "range": "stddev: 0.000027151135296069258",
            "extra": "mean: 968.3997826684648 usec\nrounds: 727"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_argus_model_instantiation",
            "value": 27175.3272269376,
            "unit": "iter/sec",
            "range": "stddev: 0.000024672656248762475",
            "extra": "mean: 36.798084955854655 usec\nrounds: 14278"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 46406.28592446627,
            "unit": "iter/sec",
            "range": "stddev: 0.000001870800699610433",
            "extra": "mean: 21.548804867247114 usec\nrounds: 20709"
          },
          {
            "name": "benchmarks/bench_batch.py::test_cqlengine_batch_insert_10",
            "value": 567.2697344198249,
            "unit": "iter/sec",
            "range": "stddev: 0.00023848409684357807",
            "extra": "mean: 1.7628298132681977 msec\nrounds: 407"
          },
          {
            "name": "benchmarks/bench_batch.py::test_coodie_batch_insert_10",
            "value": 1872.8436623870002,
            "unit": "iter/sec",
            "range": "stddev: 0.00009483702786571885",
            "extra": "mean: 533.9473977905169 usec\nrounds: 724"
          },
          {
            "name": "benchmarks/bench_batch.py::test_cqlengine_batch_insert_100",
            "value": 18.985650834957077,
            "unit": "iter/sec",
            "range": "stddev: 0.00043357960618019926",
            "extra": "mean: 52.67135736841654 msec\nrounds: 19"
          },
          {
            "name": "benchmarks/bench_batch.py::test_coodie_batch_insert_100",
            "value": 476.81369143979236,
            "unit": "iter/sec",
            "range": "stddev: 0.00042033696160794393",
            "extra": "mean: 2.0972552129960613 msec\nrounds: 277"
          },
          {
            "name": "benchmarks/bench_collections.py::test_cqlengine_collection_write",
            "value": 1595.125565068104,
            "unit": "iter/sec",
            "range": "stddev: 0.000059666215706061785",
            "extra": "mean: 626.9098946811156 usec\nrounds: 940"
          },
          {
            "name": "benchmarks/bench_collections.py::test_coodie_collection_write",
            "value": 2072.011193486987,
            "unit": "iter/sec",
            "range": "stddev: 0.000019606753317499124",
            "extra": "mean: 482.62287537023406 usec\nrounds: 1011"
          },
          {
            "name": "benchmarks/bench_collections.py::test_cqlengine_collection_read",
            "value": 1483.81414774095,
            "unit": "iter/sec",
            "range": "stddev: 0.00006348288430498113",
            "extra": "mean: 673.9388497693337 usec\nrounds: 1085"
          },
          {
            "name": "benchmarks/bench_collections.py::test_coodie_collection_read",
            "value": 2061.4277544466026,
            "unit": "iter/sec",
            "range": "stddev: 0.000017637445990508278",
            "extra": "mean: 485.10067735478486 usec\nrounds: 998"
          },
          {
            "name": "benchmarks/bench_collections.py::test_cqlengine_collection_roundtrip",
            "value": 738.6228414446708,
            "unit": "iter/sec",
            "range": "stddev: 0.00013395859890452503",
            "extra": "mean: 1.3538709391170496 msec\nrounds: 657"
          },
          {
            "name": "benchmarks/bench_collections.py::test_coodie_collection_roundtrip",
            "value": 1047.0202319811506,
            "unit": "iter/sec",
            "range": "stddev: 0.000027902567246763695",
            "extra": "mean: 955.0913816706486 usec\nrounds: 993"
          },
          {
            "name": "benchmarks/bench_delete.py::test_cqlengine_single_delete",
            "value": 895.9160562490882,
            "unit": "iter/sec",
            "range": "stddev: 0.00008652211952383249",
            "extra": "mean: 1.1161760000001313 msec\nrounds: 730"
          },
          {
            "name": "benchmarks/bench_delete.py::test_coodie_single_delete",
            "value": 1038.1529165173174,
            "unit": "iter/sec",
            "range": "stddev: 0.000019234068299037137",
            "extra": "mean: 963.2492324490031 usec\nrounds: 641"
          },
          {
            "name": "benchmarks/bench_delete.py::test_cqlengine_bulk_delete",
            "value": 864.2622490115622,
            "unit": "iter/sec",
            "range": "stddev: 0.00008437258569851066",
            "extra": "mean: 1.1570562073533561 msec\nrounds: 680"
          },
          {
            "name": "benchmarks/bench_delete.py::test_coodie_bulk_delete",
            "value": 1034.3434151254228,
            "unit": "iter/sec",
            "range": "stddev: 0.00011479039057699904",
            "extra": "mean: 966.7968929630026 usec\nrounds: 1009"
          },
          {
            "name": "benchmarks/bench_insert.py::test_cqlengine_single_insert",
            "value": 1668.2662378417963,
            "unit": "iter/sec",
            "range": "stddev: 0.00005233950112058729",
            "extra": "mean: 599.424706510683 usec\nrounds: 1029"
          },
          {
            "name": "benchmarks/bench_insert.py::test_coodie_single_insert",
            "value": 2060.1647619610917,
            "unit": "iter/sec",
            "range": "stddev: 0.000018247523238444102",
            "extra": "mean: 485.3980703213708 usec\nrounds: 1806"
          },
          {
            "name": "benchmarks/bench_insert.py::test_cqlengine_insert_if_not_exists",
            "value": 692.052857761276,
            "unit": "iter/sec",
            "range": "stddev: 0.0007183516457763385",
            "extra": "mean: 1.4449763320606799 msec\nrounds: 524"
          },
          {
            "name": "benchmarks/bench_insert.py::test_coodie_insert_if_not_exists",
            "value": 920.3567797902373,
            "unit": "iter/sec",
            "range": "stddev: 0.0000895518379852185",
            "extra": "mean: 1.0865351589281653 msec\nrounds: 560"
          },
          {
            "name": "benchmarks/bench_insert.py::test_cqlengine_insert_with_ttl",
            "value": 1632.9059701896472,
            "unit": "iter/sec",
            "range": "stddev: 0.00009872881817190053",
            "extra": "mean: 612.4051343163741 usec\nrounds: 1221"
          },
          {
            "name": "benchmarks/bench_insert.py::test_coodie_insert_with_ttl",
            "value": 2103.5022238197616,
            "unit": "iter/sec",
            "range": "stddev: 0.00001562299471872187",
            "extra": "mean: 475.39764335694133 usec\nrounds: 858"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_get_by_pk",
            "value": 1477.1715505779573,
            "unit": "iter/sec",
            "range": "stddev: 0.00007646397820312648",
            "extra": "mean: 676.9694417745458 usec\nrounds: 1082"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_get_by_pk",
            "value": 2048.8440987187823,
            "unit": "iter/sec",
            "range": "stddev: 0.000017640560506614982",
            "extra": "mean: 488.0800840948986 usec\nrounds: 1641"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_filter_secondary_index",
            "value": 212.9475160089025,
            "unit": "iter/sec",
            "range": "stddev: 0.0018049180564960582",
            "extra": "mean: 4.69599279081609 msec\nrounds: 196"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_filter_secondary_index",
            "value": 547.8929428664984,
            "unit": "iter/sec",
            "range": "stddev: 0.00005751566915012567",
            "extra": "mean: 1.8251740837692514 msec\nrounds: 382"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_filter_limit",
            "value": 848.4139082747423,
            "unit": "iter/sec",
            "range": "stddev: 0.0001481950728055678",
            "extra": "mean: 1.1786699749341798 msec\nrounds: 758"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_filter_limit",
            "value": 1497.3474516346546,
            "unit": "iter/sec",
            "range": "stddev: 0.00008716474182750792",
            "extra": "mean: 667.8476654889283 usec\nrounds: 849"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_count",
            "value": 958.997607601079,
            "unit": "iter/sec",
            "range": "stddev: 0.000057188286064177516",
            "extra": "mean: 1.0427554689124698 msec\nrounds: 772"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_count",
            "value": 1075.3877586427677,
            "unit": "iter/sec",
            "range": "stddev: 0.00003661098688277733",
            "extra": "mean: 929.897138927903 usec\nrounds: 727"
          },
          {
            "name": "benchmarks/bench_schema.py::test_cqlengine_sync_table_create",
            "value": 5829.419129777134,
            "unit": "iter/sec",
            "range": "stddev: 0.00005158139297635766",
            "extra": "mean: 171.54367832155364 usec\nrounds: 143"
          },
          {
            "name": "benchmarks/bench_schema.py::test_coodie_sync_table_create",
            "value": 46380.343776184964,
            "unit": "iter/sec",
            "range": "stddev: 0.0000034776685324127066",
            "extra": "mean: 21.56085786741134 usec\nrounds: 197"
          },
          {
            "name": "benchmarks/bench_schema.py::test_cqlengine_sync_table_noop",
            "value": 4828.66801070741,
            "unit": "iter/sec",
            "range": "stddev: 0.0000559246570724959",
            "extra": "mean: 207.09644932775115 usec\nrounds: 2753"
          },
          {
            "name": "benchmarks/bench_schema.py::test_coodie_sync_table_noop",
            "value": 51381.72667621222,
            "unit": "iter/sec",
            "range": "stddev: 0.000002388212888934256",
            "extra": "mean: 19.462171956610437 usec\nrounds: 15312"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_cqlengine_model_instantiation",
            "value": 81420.66115349192,
            "unit": "iter/sec",
            "range": "stddev: 0.000017163510061765012",
            "extra": "mean: 12.28189486345276 usec\nrounds: 22000"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 519949.69963519496,
            "unit": "iter/sec",
            "range": "stddev: 5.172779968017978e-7",
            "extra": "mean: 1.9232629631320413 usec\nrounds: 47577"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_cqlengine_model_serialization",
            "value": 219698.26099740574,
            "unit": "iter/sec",
            "range": "stddev: 0.000004890285948694013",
            "extra": "mean: 4.551697384677106 usec\nrounds: 63817"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 524525.4820295237,
            "unit": "iter/sec",
            "range": "stddev: 4.012885376486914e-7",
            "extra": "mean: 1.9064850693826034 usec\nrounds: 41693"
          },
          {
            "name": "benchmarks/bench_update.py::test_cqlengine_partial_update",
            "value": 1906.6004228170411,
            "unit": "iter/sec",
            "range": "stddev: 0.00006536512424673589",
            "extra": "mean: 524.4937471074718 usec\nrounds: 1210"
          },
          {
            "name": "benchmarks/bench_update.py::test_coodie_partial_update",
            "value": 1028.6144064287034,
            "unit": "iter/sec",
            "range": "stddev: 0.00002609321371985372",
            "extra": "mean: 972.1816005590947 usec\nrounds: 716"
          },
          {
            "name": "benchmarks/bench_update.py::test_cqlengine_update_if_condition",
            "value": 804.548890702998,
            "unit": "iter/sec",
            "range": "stddev: 0.00009317561680550098",
            "extra": "mean: 1.2429325446291037 msec\nrounds: 661"
          },
          {
            "name": "benchmarks/bench_update.py::test_coodie_update_if_condition",
            "value": 655.3756141555536,
            "unit": "iter/sec",
            "range": "stddev: 0.00009801707832286819",
            "extra": "mean: 1.5258425525772608 msec\nrounds: 485"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "ec4122a5e76ba7a394c0b3af6d6f2148c5313eaf",
          "message": "fix(ci): strip copilot agent steps from squash commit messages\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-02-25T21:51:41+02:00",
          "tree_id": "2e64837a833487e83ff79abc69b7ce6a3fe7bda1",
          "url": "https://github.com/fruch/coodie/commit/ec4122a5e76ba7a394c0b3af6d6f2148c5313eaf"
        },
        "date": 1772049175983,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_get_or_create_user",
            "value": 1366.378553207217,
            "unit": "iter/sec",
            "range": "stddev: 0.0002145732664516196",
            "extra": "mean: 731.8616042770585 usec\nrounds: 561"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_get_or_create_user",
            "value": 2063.455400666109,
            "unit": "iter/sec",
            "range": "stddev: 0.0000184536025713664",
            "extra": "mean: 484.62399510897467 usec\nrounds: 818"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_filter_runs_by_status",
            "value": 920.4227925477323,
            "unit": "iter/sec",
            "range": "stddev: 0.0006783693242211733",
            "extra": "mean: 1.0864572325854704 msec\nrounds: 890"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_filter_runs_by_status",
            "value": 2080.819287018901,
            "unit": "iter/sec",
            "range": "stddev: 0.00002538758089634712",
            "extra": "mean: 480.57993610423347 usec\nrounds: 986"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_latest_runs",
            "value": 1071.1697180584804,
            "unit": "iter/sec",
            "range": "stddev: 0.00007807206875584689",
            "extra": "mean: 933.5588778709342 usec\nrounds: 958"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_latest_runs",
            "value": 2096.016940225524,
            "unit": "iter/sec",
            "range": "stddev: 0.000020288655721084672",
            "extra": "mean: 477.095380675885 usec\nrounds: 1035"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_list_mutation",
            "value": 1348.838116632142,
            "unit": "iter/sec",
            "range": "stddev: 0.00007414370360932457",
            "extra": "mean: 741.3788116374251 usec\nrounds: 653"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_list_mutation",
            "value": 1039.698350861754,
            "unit": "iter/sec",
            "range": "stddev: 0.00002971357100404663",
            "extra": "mean: 961.8174340385841 usec\nrounds: 993"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_batch_events",
            "value": 329.6553733654116,
            "unit": "iter/sec",
            "range": "stddev: 0.00018131364818716142",
            "extra": "mean: 3.0334709542002054 msec\nrounds: 262"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_batch_events",
            "value": 869.2753943988514,
            "unit": "iter/sec",
            "range": "stddev: 0.000048029841348253826",
            "extra": "mean: 1.1503834186996071 msec\nrounds: 492"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_notification_feed",
            "value": 734.9293065586835,
            "unit": "iter/sec",
            "range": "stddev: 0.00011888472870247307",
            "extra": "mean: 1.360675089530058 msec\nrounds: 659"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_notification_feed",
            "value": 1483.0258157958735,
            "unit": "iter/sec",
            "range": "stddev: 0.00007190254740529937",
            "extra": "mean: 674.2970954037943 usec\nrounds: 870"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_status_update",
            "value": 1192.9651113312675,
            "unit": "iter/sec",
            "range": "stddev: 0.00007305254705808406",
            "extra": "mean: 838.2474814238853 usec\nrounds: 646"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_status_update",
            "value": 1045.575751703445,
            "unit": "iter/sec",
            "range": "stddev: 0.000018020294288903996",
            "extra": "mean: 956.4108562873677 usec\nrounds: 668"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_comment_with_collections",
            "value": 1325.677002928398,
            "unit": "iter/sec",
            "range": "stddev: 0.00006463086251784166",
            "extra": "mean: 754.3315587364168 usec\nrounds: 664"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_comment_with_collections",
            "value": 2022.3632878494361,
            "unit": "iter/sec",
            "range": "stddev: 0.000022210347838956402",
            "extra": "mean: 494.47100133200667 usec\nrounds: 750"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_multi_model_lookup",
            "value": 736.9426034406953,
            "unit": "iter/sec",
            "range": "stddev: 0.0001049627225556626",
            "extra": "mean: 1.3569577811502846 msec\nrounds: 626"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_multi_model_lookup",
            "value": 1041.531711282909,
            "unit": "iter/sec",
            "range": "stddev: 0.000022895448610423515",
            "extra": "mean: 960.1243909974162 usec\nrounds: 711"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_argus_model_instantiation",
            "value": 26894.52619365739,
            "unit": "iter/sec",
            "range": "stddev: 0.000025448512691274615",
            "extra": "mean: 37.182287310041275 usec\nrounds: 10386"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 46480.645602157434,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019470411447578187",
            "extra": "mean: 21.51433111663974 usec\nrounds: 18498"
          },
          {
            "name": "benchmarks/bench_batch.py::test_cqlengine_batch_insert_10",
            "value": 596.6583905704443,
            "unit": "iter/sec",
            "range": "stddev: 0.00009451052019431654",
            "extra": "mean: 1.6760009006894794 msec\nrounds: 433"
          },
          {
            "name": "benchmarks/bench_batch.py::test_coodie_batch_insert_10",
            "value": 1754.5621160517273,
            "unit": "iter/sec",
            "range": "stddev: 0.00016870460035038395",
            "extra": "mean: 569.942774240612 usec\nrounds: 691"
          },
          {
            "name": "benchmarks/bench_batch.py::test_cqlengine_batch_insert_100",
            "value": 18.743410340997972,
            "unit": "iter/sec",
            "range": "stddev: 0.0006937762567577873",
            "extra": "mean: 53.35208384211025 msec\nrounds: 19"
          },
          {
            "name": "benchmarks/bench_batch.py::test_coodie_batch_insert_100",
            "value": 503.82465123451976,
            "unit": "iter/sec",
            "range": "stddev: 0.00027830525341537393",
            "extra": "mean: 1.9848175303643907 msec\nrounds: 247"
          },
          {
            "name": "benchmarks/bench_collections.py::test_cqlengine_collection_write",
            "value": 1392.058323499551,
            "unit": "iter/sec",
            "range": "stddev: 0.00023403171964346355",
            "extra": "mean: 718.3607059552361 usec\nrounds: 806"
          },
          {
            "name": "benchmarks/bench_collections.py::test_coodie_collection_write",
            "value": 2042.8914951266145,
            "unit": "iter/sec",
            "range": "stddev: 0.000017191836668000803",
            "extra": "mean: 489.5022581402552 usec\nrounds: 860"
          },
          {
            "name": "benchmarks/bench_collections.py::test_cqlengine_collection_read",
            "value": 1526.041742575589,
            "unit": "iter/sec",
            "range": "stddev: 0.00006096411752414444",
            "extra": "mean: 655.2900697934003 usec\nrounds: 874"
          },
          {
            "name": "benchmarks/bench_collections.py::test_coodie_collection_read",
            "value": 2097.602751101088,
            "unit": "iter/sec",
            "range": "stddev: 0.00001745126075060178",
            "extra": "mean: 476.7346912922731 usec\nrounds: 758"
          },
          {
            "name": "benchmarks/bench_collections.py::test_cqlengine_collection_roundtrip",
            "value": 761.5735060085475,
            "unit": "iter/sec",
            "range": "stddev: 0.00008986238602395515",
            "extra": "mean: 1.3130708882469666 msec\nrounds: 519"
          },
          {
            "name": "benchmarks/bench_collections.py::test_coodie_collection_roundtrip",
            "value": 1037.8721388885783,
            "unit": "iter/sec",
            "range": "stddev: 0.000022435732342853496",
            "extra": "mean: 963.5098221933829 usec\nrounds: 793"
          },
          {
            "name": "benchmarks/bench_delete.py::test_cqlengine_single_delete",
            "value": 960.648857561155,
            "unit": "iter/sec",
            "range": "stddev: 0.00007236447441441221",
            "extra": "mean: 1.0409630866982424 msec\nrounds: 669"
          },
          {
            "name": "benchmarks/bench_delete.py::test_coodie_single_delete",
            "value": 1040.0706730248517,
            "unit": "iter/sec",
            "range": "stddev: 0.000022084433495270154",
            "extra": "mean: 961.4731247941896 usec\nrounds: 609"
          },
          {
            "name": "benchmarks/bench_delete.py::test_cqlengine_bulk_delete",
            "value": 882.5018350548645,
            "unit": "iter/sec",
            "range": "stddev: 0.0000822236328578166",
            "extra": "mean: 1.1331421196850324 msec\nrounds: 635"
          },
          {
            "name": "benchmarks/bench_delete.py::test_coodie_bulk_delete",
            "value": 1035.4263910372374,
            "unit": "iter/sec",
            "range": "stddev: 0.000023384297135537534",
            "extra": "mean: 965.7856981974845 usec\nrounds: 888"
          },
          {
            "name": "benchmarks/bench_insert.py::test_cqlengine_single_insert",
            "value": 1655.808851302593,
            "unit": "iter/sec",
            "range": "stddev: 0.00005886321199238992",
            "extra": "mean: 603.9344452189147 usec\nrounds: 1004"
          },
          {
            "name": "benchmarks/bench_insert.py::test_coodie_single_insert",
            "value": 2068.6682749068286,
            "unit": "iter/sec",
            "range": "stddev: 0.000018774315703236685",
            "extra": "mean: 483.4027824229282 usec\nrounds: 1411"
          },
          {
            "name": "benchmarks/bench_insert.py::test_cqlengine_insert_if_not_exists",
            "value": 622.5854226771656,
            "unit": "iter/sec",
            "range": "stddev: 0.0004381977571796574",
            "extra": "mean: 1.6062052909943225 msec\nrounds: 433"
          },
          {
            "name": "benchmarks/bench_insert.py::test_coodie_insert_if_not_exists",
            "value": 725.4421520215194,
            "unit": "iter/sec",
            "range": "stddev: 0.0003226061431671621",
            "extra": "mean: 1.378469664622323 msec\nrounds: 489"
          },
          {
            "name": "benchmarks/bench_insert.py::test_cqlengine_insert_with_ttl",
            "value": 1657.9831695604005,
            "unit": "iter/sec",
            "range": "stddev: 0.00006531878376407532",
            "extra": "mean: 603.1424313342947 usec\nrounds: 1034"
          },
          {
            "name": "benchmarks/bench_insert.py::test_coodie_insert_with_ttl",
            "value": 1962.5927081742598,
            "unit": "iter/sec",
            "range": "stddev: 0.00011798618786305347",
            "extra": "mean: 509.5300700114541 usec\nrounds: 857"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_get_by_pk",
            "value": 1516.4422541783008,
            "unit": "iter/sec",
            "range": "stddev: 0.00006790323397305778",
            "extra": "mean: 659.4382326426665 usec\nrounds: 821"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_get_by_pk",
            "value": 2102.242999043518,
            "unit": "iter/sec",
            "range": "stddev: 0.00001770110066617919",
            "extra": "mean: 475.6824022983934 usec\nrounds: 1392"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_filter_secondary_index",
            "value": 217.80362049382066,
            "unit": "iter/sec",
            "range": "stddev: 0.0005926164317296756",
            "extra": "mean: 4.5912919065933115 msec\nrounds: 182"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_filter_secondary_index",
            "value": 555.7813256287491,
            "unit": "iter/sec",
            "range": "stddev: 0.00005495162021535879",
            "extra": "mean: 1.7992688021115344 msec\nrounds: 379"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_filter_limit",
            "value": 887.3764700876034,
            "unit": "iter/sec",
            "range": "stddev: 0.0001501626830815462",
            "extra": "mean: 1.1269174174758974 msec\nrounds: 618"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_filter_limit",
            "value": 1424.3935789971881,
            "unit": "iter/sec",
            "range": "stddev: 0.000026019831118277447",
            "extra": "mean: 702.0531507197802 usec\nrounds: 763"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_count",
            "value": 982.2105222392684,
            "unit": "iter/sec",
            "range": "stddev: 0.000047849574502201144",
            "extra": "mean: 1.01811167500036 msec\nrounds: 600"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_count",
            "value": 1048.8249712557756,
            "unit": "iter/sec",
            "range": "stddev: 0.00003544506004833907",
            "extra": "mean: 953.4479321203454 usec\nrounds: 604"
          },
          {
            "name": "benchmarks/bench_schema.py::test_cqlengine_sync_table_create",
            "value": 5768.769620580974,
            "unit": "iter/sec",
            "range": "stddev: 0.00004594644368499354",
            "extra": "mean: 173.3471893958715 usec\nrounds: 132"
          },
          {
            "name": "benchmarks/bench_schema.py::test_coodie_sync_table_create",
            "value": 43863.27524632899,
            "unit": "iter/sec",
            "range": "stddev: 0.000005354268044401152",
            "extra": "mean: 22.798115151779324 usec\nrounds: 165"
          },
          {
            "name": "benchmarks/bench_schema.py::test_cqlengine_sync_table_noop",
            "value": 4404.902791427427,
            "unit": "iter/sec",
            "range": "stddev: 0.0005557682501668238",
            "extra": "mean: 227.0197657814705 usec\nrounds: 2788"
          },
          {
            "name": "benchmarks/bench_schema.py::test_coodie_sync_table_noop",
            "value": 47530.67382932602,
            "unit": "iter/sec",
            "range": "stddev: 0.000013415495477981412",
            "extra": "mean: 21.039045303477447 usec\nrounds: 7218"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_cqlengine_model_instantiation",
            "value": 82454.54533191455,
            "unit": "iter/sec",
            "range": "stddev: 0.000017686601066512073",
            "extra": "mean: 12.127894174597355 usec\nrounds: 25098"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 485469.49937551026,
            "unit": "iter/sec",
            "range": "stddev: 4.2587762060914093e-7",
            "extra": "mean: 2.0598616417434306 usec\nrounds: 38899"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_cqlengine_model_serialization",
            "value": 221127.22538732813,
            "unit": "iter/sec",
            "range": "stddev: 6.237869348795964e-7",
            "extra": "mean: 4.522283487473748 usec\nrounds: 46316"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 512042.1427968825,
            "unit": "iter/sec",
            "range": "stddev: 4.189943809549841e-7",
            "extra": "mean: 1.952964251219223 usec\nrounds: 37148"
          },
          {
            "name": "benchmarks/bench_update.py::test_cqlengine_partial_update",
            "value": 1917.9037128077862,
            "unit": "iter/sec",
            "range": "stddev: 0.000067652693601016",
            "extra": "mean: 521.4026091727061 usec\nrounds: 1003"
          },
          {
            "name": "benchmarks/bench_update.py::test_coodie_partial_update",
            "value": 1022.8469137293849,
            "unit": "iter/sec",
            "range": "stddev: 0.00002691351641376058",
            "extra": "mean: 977.6634084507493 usec\nrounds: 568"
          },
          {
            "name": "benchmarks/bench_update.py::test_cqlengine_update_if_condition",
            "value": 602.0410764763267,
            "unit": "iter/sec",
            "range": "stddev: 0.0009820203147879606",
            "extra": "mean: 1.6610162314054693 msec\nrounds: 484"
          },
          {
            "name": "benchmarks/bench_update.py::test_coodie_update_if_condition",
            "value": 533.4789987630502,
            "unit": "iter/sec",
            "range": "stddev: 0.00028719445574243755",
            "extra": "mean: 1.8744880348029587 msec\nrounds: 431"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "442096c4a3e798d7492ad0d50ab083a1b9b65b3c",
          "message": "docs: add full Phase A UDT support implementation plan\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-02-25T22:45:05+02:00",
          "tree_id": "735d055c749fcc93f1e099eccb6e3799f3d77e09",
          "url": "https://github.com/fruch/coodie/commit/442096c4a3e798d7492ad0d50ab083a1b9b65b3c"
        },
        "date": 1772052377455,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_get_or_create_user",
            "value": 1413.1923502472227,
            "unit": "iter/sec",
            "range": "stddev: 0.0001229187698479311",
            "extra": "mean: 707.6177562276365 usec\nrounds: 562"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_get_or_create_user",
            "value": 2076.359434817097,
            "unit": "iter/sec",
            "range": "stddev: 0.00002254391097245365",
            "extra": "mean: 481.6121829542911 usec\nrounds: 880"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_filter_runs_by_status",
            "value": 863.7590181603583,
            "unit": "iter/sec",
            "range": "stddev: 0.0009302710588529338",
            "extra": "mean: 1.1577303147929026 msec\nrounds: 845"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_filter_runs_by_status",
            "value": 2050.8244791261845,
            "unit": "iter/sec",
            "range": "stddev: 0.00003582695087041851",
            "extra": "mean: 487.60876914541217 usec\nrounds: 901"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_latest_runs",
            "value": 1042.332630820897,
            "unit": "iter/sec",
            "range": "stddev: 0.00010844148495900224",
            "extra": "mean: 959.3866395724772 usec\nrounds: 935"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_latest_runs",
            "value": 2062.8911093318397,
            "unit": "iter/sec",
            "range": "stddev: 0.000024343158051925636",
            "extra": "mean: 484.75656105953897 usec\nrounds: 868"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_list_mutation",
            "value": 1302.9570973641364,
            "unit": "iter/sec",
            "range": "stddev: 0.00009051392132316108",
            "extra": "mean: 767.4849786097989 usec\nrounds: 561"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_list_mutation",
            "value": 1030.144621163517,
            "unit": "iter/sec",
            "range": "stddev: 0.000027083258943437",
            "extra": "mean: 970.7374862284194 usec\nrounds: 944"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_batch_events",
            "value": 320.4627130754362,
            "unit": "iter/sec",
            "range": "stddev: 0.0002569723266322797",
            "extra": "mean: 3.120487842105369 msec\nrounds: 247"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_batch_events",
            "value": 853.597794225434,
            "unit": "iter/sec",
            "range": "stddev: 0.00007408844797248287",
            "extra": "mean: 1.1715119307535389 msec\nrounds: 491"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_notification_feed",
            "value": 717.0288658376345,
            "unit": "iter/sec",
            "range": "stddev: 0.00015679672395800233",
            "extra": "mean: 1.3946439922356515 msec\nrounds: 644"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_notification_feed",
            "value": 1427.6125186154263,
            "unit": "iter/sec",
            "range": "stddev: 0.000031109096264180766",
            "extra": "mean: 700.4701814816337 usec\nrounds: 810"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_status_update",
            "value": 1119.4637657289227,
            "unit": "iter/sec",
            "range": "stddev: 0.00010052308816446823",
            "extra": "mean: 893.2848303034306 usec\nrounds: 495"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_status_update",
            "value": 1031.7646493655825,
            "unit": "iter/sec",
            "range": "stddev: 0.000031917917573080586",
            "extra": "mean: 969.2132800003235 usec\nrounds: 575"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_comment_with_collections",
            "value": 1258.3235544653185,
            "unit": "iter/sec",
            "range": "stddev: 0.00009362144351753767",
            "extra": "mean: 794.7081626592582 usec\nrounds: 707"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_comment_with_collections",
            "value": 2012.049733153231,
            "unit": "iter/sec",
            "range": "stddev: 0.00003231216898208067",
            "extra": "mean: 497.00560752682117 usec\nrounds: 744"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_multi_model_lookup",
            "value": 700.3786916485274,
            "unit": "iter/sec",
            "range": "stddev: 0.00013209827681811016",
            "extra": "mean: 1.427799006343603 msec\nrounds: 473"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_multi_model_lookup",
            "value": 1024.9411080894859,
            "unit": "iter/sec",
            "range": "stddev: 0.000025272654747449923",
            "extra": "mean: 975.6658134866143 usec\nrounds: 697"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_argus_model_instantiation",
            "value": 27101.91607143915,
            "unit": "iter/sec",
            "range": "stddev: 0.000026202512551326825",
            "extra": "mean: 36.897760193930765 usec\nrounds: 11968"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 46780.91647747179,
            "unit": "iter/sec",
            "range": "stddev: 0.000002696348303279986",
            "extra": "mean: 21.376237904222513 usec\nrounds: 18188"
          },
          {
            "name": "benchmarks/bench_batch.py::test_cqlengine_batch_insert_10",
            "value": 573.6006772122719,
            "unit": "iter/sec",
            "range": "stddev: 0.0001247545143723744",
            "extra": "mean: 1.7433731160500896 msec\nrounds: 405"
          },
          {
            "name": "benchmarks/bench_batch.py::test_coodie_batch_insert_10",
            "value": 1607.6145508812506,
            "unit": "iter/sec",
            "range": "stddev: 0.000171801855156754",
            "extra": "mean: 622.0396546248148 usec\nrounds: 692"
          },
          {
            "name": "benchmarks/bench_batch.py::test_cqlengine_batch_insert_100",
            "value": 18.445295835720277,
            "unit": "iter/sec",
            "range": "stddev: 0.0008227588981597571",
            "extra": "mean: 54.21436494737308 msec\nrounds: 19"
          },
          {
            "name": "benchmarks/bench_batch.py::test_coodie_batch_insert_100",
            "value": 486.6058659679398,
            "unit": "iter/sec",
            "range": "stddev: 0.0002092162147318298",
            "extra": "mean: 2.0550512641495478 msec\nrounds: 212"
          },
          {
            "name": "benchmarks/bench_collections.py::test_cqlengine_collection_write",
            "value": 1499.1841612285518,
            "unit": "iter/sec",
            "range": "stddev: 0.00008653526422899674",
            "extra": "mean: 667.0294589962314 usec\nrounds: 756"
          },
          {
            "name": "benchmarks/bench_collections.py::test_coodie_collection_write",
            "value": 2055.51220215627,
            "unit": "iter/sec",
            "range": "stddev: 0.00002072311298445747",
            "extra": "mean: 486.4967471129491 usec\nrounds: 866"
          },
          {
            "name": "benchmarks/bench_collections.py::test_cqlengine_collection_read",
            "value": 1471.9173991498722,
            "unit": "iter/sec",
            "range": "stddev: 0.00008389938800448778",
            "extra": "mean: 679.3859496311171 usec\nrounds: 814"
          },
          {
            "name": "benchmarks/bench_collections.py::test_coodie_collection_read",
            "value": 2046.0246288294486,
            "unit": "iter/sec",
            "range": "stddev: 0.000018987360788779443",
            "extra": "mean: 488.75266988946765 usec\nrounds: 724"
          },
          {
            "name": "benchmarks/bench_collections.py::test_cqlengine_collection_roundtrip",
            "value": 722.2564983957951,
            "unit": "iter/sec",
            "range": "stddev: 0.00016504525290785875",
            "extra": "mean: 1.3845496748331116 msec\nrounds: 449"
          },
          {
            "name": "benchmarks/bench_collections.py::test_coodie_collection_roundtrip",
            "value": 1013.3950574507822,
            "unit": "iter/sec",
            "range": "stddev: 0.000056576269949415464",
            "extra": "mean: 986.7819984395051 usec\nrounds: 641"
          },
          {
            "name": "benchmarks/bench_delete.py::test_cqlengine_single_delete",
            "value": 871.6802246492933,
            "unit": "iter/sec",
            "range": "stddev: 0.00011457657466159067",
            "extra": "mean: 1.1472096896569313 msec\nrounds: 406"
          },
          {
            "name": "benchmarks/bench_delete.py::test_coodie_single_delete",
            "value": 1039.9165894107764,
            "unit": "iter/sec",
            "range": "stddev: 0.0000510599412528035",
            "extra": "mean: 961.6155855024936 usec\nrounds: 538"
          },
          {
            "name": "benchmarks/bench_delete.py::test_cqlengine_bulk_delete",
            "value": 824.2754570660298,
            "unit": "iter/sec",
            "range": "stddev: 0.00011867628358124353",
            "extra": "mean: 1.2131866737358084 msec\nrounds: 613"
          },
          {
            "name": "benchmarks/bench_delete.py::test_coodie_bulk_delete",
            "value": 1034.3174265333976,
            "unit": "iter/sec",
            "range": "stddev: 0.00002374255522189207",
            "extra": "mean: 966.8211850124044 usec\nrounds: 854"
          },
          {
            "name": "benchmarks/bench_insert.py::test_cqlengine_single_insert",
            "value": 1553.5523533109324,
            "unit": "iter/sec",
            "range": "stddev: 0.00008213675116492982",
            "extra": "mean: 643.68606430855 usec\nrounds: 933"
          },
          {
            "name": "benchmarks/bench_insert.py::test_coodie_single_insert",
            "value": 2077.0738032815334,
            "unit": "iter/sec",
            "range": "stddev: 0.00001944586146537558",
            "extra": "mean: 481.44654196693307 usec\nrounds: 1251"
          },
          {
            "name": "benchmarks/bench_insert.py::test_cqlengine_insert_if_not_exists",
            "value": 725.442041306858,
            "unit": "iter/sec",
            "range": "stddev: 0.0003126701218426249",
            "extra": "mean: 1.378469874999987 msec\nrounds: 424"
          },
          {
            "name": "benchmarks/bench_insert.py::test_coodie_insert_if_not_exists",
            "value": 826.5283111583238,
            "unit": "iter/sec",
            "range": "stddev: 0.00046934425159640534",
            "extra": "mean: 1.2098799115526573 msec\nrounds: 554"
          },
          {
            "name": "benchmarks/bench_insert.py::test_cqlengine_insert_with_ttl",
            "value": 1587.7211609053923,
            "unit": "iter/sec",
            "range": "stddev: 0.00007965089126184959",
            "extra": "mean: 629.8335152437936 usec\nrounds: 984"
          },
          {
            "name": "benchmarks/bench_insert.py::test_coodie_insert_with_ttl",
            "value": 2067.4359750787526,
            "unit": "iter/sec",
            "range": "stddev: 0.00002291472620947657",
            "extra": "mean: 483.69091573048985 usec\nrounds: 890"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_get_by_pk",
            "value": 1412.0975523019742,
            "unit": "iter/sec",
            "range": "stddev: 0.0001014088304880508",
            "extra": "mean: 708.1663716290841 usec\nrounds: 853"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_get_by_pk",
            "value": 2056.686552260253,
            "unit": "iter/sec",
            "range": "stddev: 0.000018598439028110548",
            "extra": "mean: 486.21896170859 usec\nrounds: 1358"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_filter_secondary_index",
            "value": 205.72527953143887,
            "unit": "iter/sec",
            "range": "stddev: 0.0005906222855938386",
            "extra": "mean: 4.860851336683591 msec\nrounds: 199"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_filter_secondary_index",
            "value": 538.1418584892899,
            "unit": "iter/sec",
            "range": "stddev: 0.00005384701367694893",
            "extra": "mean: 1.858246081818038 msec\nrounds: 330"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_filter_limit",
            "value": 858.2450483968893,
            "unit": "iter/sec",
            "range": "stddev: 0.00013859752022814934",
            "extra": "mean: 1.1651683885248088 msec\nrounds: 610"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_filter_limit",
            "value": 1405.612957100098,
            "unit": "iter/sec",
            "range": "stddev: 0.00005186871756223176",
            "extra": "mean: 711.433396333431 usec\nrounds: 709"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_count",
            "value": 937.0597576123811,
            "unit": "iter/sec",
            "range": "stddev: 0.00008806989910609005",
            "extra": "mean: 1.0671678000002798 msec\nrounds: 565"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_count",
            "value": 1056.184753255331,
            "unit": "iter/sec",
            "range": "stddev: 0.000050101165108164594",
            "extra": "mean: 946.8040481722912 usec\nrounds: 602"
          },
          {
            "name": "benchmarks/bench_schema.py::test_cqlengine_sync_table_create",
            "value": 5564.386191209431,
            "unit": "iter/sec",
            "range": "stddev: 0.00007855500606894048",
            "extra": "mean: 179.71434146317728 usec\nrounds: 123"
          },
          {
            "name": "benchmarks/bench_schema.py::test_coodie_sync_table_create",
            "value": 40561.43847708143,
            "unit": "iter/sec",
            "range": "stddev: 0.000007991745299996036",
            "extra": "mean: 24.653957984380497 usec\nrounds: 119"
          },
          {
            "name": "benchmarks/bench_schema.py::test_cqlengine_sync_table_noop",
            "value": 4226.003753556559,
            "unit": "iter/sec",
            "range": "stddev: 0.0005975370718390449",
            "extra": "mean: 236.63017316499324 usec\nrounds: 3078"
          },
          {
            "name": "benchmarks/bench_schema.py::test_coodie_sync_table_noop",
            "value": 48258.294570677586,
            "unit": "iter/sec",
            "range": "stddev: 0.000012971108257078535",
            "extra": "mean: 20.72182634915603 usec\nrounds: 7302"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_cqlengine_model_instantiation",
            "value": 81038.56590338913,
            "unit": "iter/sec",
            "range": "stddev: 0.000018281878824669683",
            "extra": "mean: 12.339803757042779 usec\nrounds: 20974"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 479059.17012938595,
            "unit": "iter/sec",
            "range": "stddev: 5.071760821083286e-7",
            "extra": "mean: 2.0874248158738236 usec\nrounds: 37468"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_cqlengine_model_serialization",
            "value": 222501.3015728617,
            "unit": "iter/sec",
            "range": "stddev: 7.637480322296098e-7",
            "extra": "mean: 4.49435573154404 usec\nrounds: 46209"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 507123.25973625085,
            "unit": "iter/sec",
            "range": "stddev: 6.005561009541723e-7",
            "extra": "mean: 1.971907185878417 usec\nrounds: 33928"
          },
          {
            "name": "benchmarks/bench_update.py::test_cqlengine_partial_update",
            "value": 1835.2383184806308,
            "unit": "iter/sec",
            "range": "stddev: 0.00008052510956623768",
            "extra": "mean: 544.8883613262209 usec\nrounds: 905"
          },
          {
            "name": "benchmarks/bench_update.py::test_coodie_partial_update",
            "value": 1035.3844919456612,
            "unit": "iter/sec",
            "range": "stddev: 0.000027735403909380864",
            "extra": "mean: 965.8247808220809 usec\nrounds: 511"
          },
          {
            "name": "benchmarks/bench_update.py::test_cqlengine_update_if_condition",
            "value": 752.1099061908989,
            "unit": "iter/sec",
            "range": "stddev: 0.0003139480417832305",
            "extra": "mean: 1.3295929115793115 msec\nrounds: 475"
          },
          {
            "name": "benchmarks/bench_update.py::test_coodie_update_if_condition",
            "value": 633.2364786412845,
            "unit": "iter/sec",
            "range": "stddev: 0.0003768531479632409",
            "extra": "mean: 1.5791888713449806 msec\nrounds: 342"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "b7f8827b040c6de33ace6f9a4f82397efec7f5ab",
          "message": "docs: add §14 Cython/Rust/native extension evaluation to performance plan\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-02-25T22:47:58+02:00",
          "tree_id": "852e20449f722a3a8066049d1047a0a92aaaeb69",
          "url": "https://github.com/fruch/coodie/commit/b7f8827b040c6de33ace6f9a4f82397efec7f5ab"
        },
        "date": 1772052548924,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_get_or_create_user",
            "value": 1407.8342275110895,
            "unit": "iter/sec",
            "range": "stddev: 0.00009421904183979313",
            "extra": "mean: 710.3109019929856 usec\nrounds: 602"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_get_or_create_user",
            "value": 2089.1130117152106,
            "unit": "iter/sec",
            "range": "stddev: 0.000018649308686959878",
            "extra": "mean: 478.67204617091375 usec\nrounds: 888"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_filter_runs_by_status",
            "value": 896.2593843727096,
            "unit": "iter/sec",
            "range": "stddev: 0.0007438203753368779",
            "extra": "mean: 1.1157484288991832 msec\nrounds: 872"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_filter_runs_by_status",
            "value": 2049.1672848366607,
            "unit": "iter/sec",
            "range": "stddev: 0.000025890465515550926",
            "extra": "mean: 488.0031061396288 usec\nrounds: 961"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_latest_runs",
            "value": 1093.6992349664865,
            "unit": "iter/sec",
            "range": "stddev: 0.00008080748973761762",
            "extra": "mean: 914.3281516793256 usec\nrounds: 923"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_latest_runs",
            "value": 2090.0793335093654,
            "unit": "iter/sec",
            "range": "stddev: 0.000019990493864823053",
            "extra": "mean: 478.4507381932444 usec\nrounds: 974"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_list_mutation",
            "value": 1325.560236207198,
            "unit": "iter/sec",
            "range": "stddev: 0.00007682522951634737",
            "extra": "mean: 754.3980067335773 usec\nrounds: 594"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_list_mutation",
            "value": 1043.5077860122476,
            "unit": "iter/sec",
            "range": "stddev: 0.00002563311768550833",
            "extra": "mean: 958.3062181275023 usec\nrounds: 1004"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_batch_events",
            "value": 334.6995739790375,
            "unit": "iter/sec",
            "range": "stddev: 0.00012021151192273041",
            "extra": "mean: 2.9877540270267295 msec\nrounds: 259"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_batch_events",
            "value": 849.6773406093052,
            "unit": "iter/sec",
            "range": "stddev: 0.0001279464721103755",
            "extra": "mean: 1.1769173452158888 msec\nrounds: 533"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_notification_feed",
            "value": 738.8487457950006,
            "unit": "iter/sec",
            "range": "stddev: 0.00011744044352143188",
            "extra": "mean: 1.3534569906104408 msec\nrounds: 639"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_notification_feed",
            "value": 1432.747233502476,
            "unit": "iter/sec",
            "range": "stddev: 0.00003677606858406887",
            "extra": "mean: 697.9598191618298 usec\nrounds: 835"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_status_update",
            "value": 1178.0709798467556,
            "unit": "iter/sec",
            "range": "stddev: 0.00007603880136610164",
            "extra": "mean: 848.8452878536069 usec\nrounds: 601"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_status_update",
            "value": 1034.0020778739345,
            "unit": "iter/sec",
            "range": "stddev: 0.00002539387490806531",
            "extra": "mean: 967.116044927252 usec\nrounds: 690"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_comment_with_collections",
            "value": 1322.2757706311625,
            "unit": "iter/sec",
            "range": "stddev: 0.00006563950970649203",
            "extra": "mean: 756.2718929067796 usec\nrounds: 719"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_comment_with_collections",
            "value": 2045.834213213231,
            "unit": "iter/sec",
            "range": "stddev: 0.000022320022132707518",
            "extra": "mean: 488.79816044789794 usec\nrounds: 804"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_multi_model_lookup",
            "value": 721.9773383111896,
            "unit": "iter/sec",
            "range": "stddev: 0.00010599880631095503",
            "extra": "mean: 1.3850850254374272 msec\nrounds: 629"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_multi_model_lookup",
            "value": 1046.320618964634,
            "unit": "iter/sec",
            "range": "stddev: 0.000021629386685266654",
            "extra": "mean: 955.7299950654995 usec\nrounds: 608"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_argus_model_instantiation",
            "value": 26920.382443108934,
            "unit": "iter/sec",
            "range": "stddev: 0.000024149868437650174",
            "extra": "mean: 37.14657479749064 usec\nrounds: 11110"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 46959.179610608975,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017104641892171201",
            "extra": "mean: 21.295090934128687 usec\nrounds: 18178"
          },
          {
            "name": "benchmarks/bench_batch.py::test_cqlengine_batch_insert_10",
            "value": 590.2129550720277,
            "unit": "iter/sec",
            "range": "stddev: 0.00012201482995515105",
            "extra": "mean: 1.6943037109003531 msec\nrounds: 422"
          },
          {
            "name": "benchmarks/bench_batch.py::test_coodie_batch_insert_10",
            "value": 1806.9561585715505,
            "unit": "iter/sec",
            "range": "stddev: 0.0000965791149768305",
            "extra": "mean: 553.4168580993842 usec\nrounds: 747"
          },
          {
            "name": "benchmarks/bench_batch.py::test_cqlengine_batch_insert_100",
            "value": 18.77745194912559,
            "unit": "iter/sec",
            "range": "stddev: 0.00045040574746711524",
            "extra": "mean: 53.255361947368314 msec\nrounds: 19"
          },
          {
            "name": "benchmarks/bench_batch.py::test_coodie_batch_insert_100",
            "value": 494.85893409849746,
            "unit": "iter/sec",
            "range": "stddev: 0.00036128716678281413",
            "extra": "mean: 2.0207779047613568 msec\nrounds: 252"
          },
          {
            "name": "benchmarks/bench_collections.py::test_cqlengine_collection_write",
            "value": 1330.9397237727724,
            "unit": "iter/sec",
            "range": "stddev: 0.00028830146328322735",
            "extra": "mean: 751.3488268013609 usec\nrounds: 791"
          },
          {
            "name": "benchmarks/bench_collections.py::test_coodie_collection_write",
            "value": 2068.929297516645,
            "unit": "iter/sec",
            "range": "stddev: 0.000021731293148541766",
            "extra": "mean: 483.34179481160106 usec\nrounds: 848"
          },
          {
            "name": "benchmarks/bench_collections.py::test_cqlengine_collection_read",
            "value": 1472.9629545749763,
            "unit": "iter/sec",
            "range": "stddev: 0.00007120132059045239",
            "extra": "mean: 678.9037001195663 usec\nrounds: 837"
          },
          {
            "name": "benchmarks/bench_collections.py::test_coodie_collection_read",
            "value": 2092.787043849033,
            "unit": "iter/sec",
            "range": "stddev: 0.00001699125562348904",
            "extra": "mean: 477.83170434809745 usec\nrounds: 805"
          },
          {
            "name": "benchmarks/bench_collections.py::test_cqlengine_collection_roundtrip",
            "value": 725.9215611685617,
            "unit": "iter/sec",
            "range": "stddev: 0.00013095675358459734",
            "extra": "mean: 1.3775593032258706 msec\nrounds: 465"
          },
          {
            "name": "benchmarks/bench_collections.py::test_coodie_collection_roundtrip",
            "value": 1029.837586752865,
            "unit": "iter/sec",
            "range": "stddev: 0.00002626115107895575",
            "extra": "mean: 971.0269006135767 usec\nrounds: 815"
          },
          {
            "name": "benchmarks/bench_delete.py::test_cqlengine_single_delete",
            "value": 898.9643050220692,
            "unit": "iter/sec",
            "range": "stddev: 0.00009261656591082709",
            "extra": "mean: 1.1123912200000536 msec\nrounds: 600"
          },
          {
            "name": "benchmarks/bench_delete.py::test_coodie_single_delete",
            "value": 1035.545866710358,
            "unit": "iter/sec",
            "range": "stddev: 0.0000262479863656394",
            "extra": "mean: 965.6742710747546 usec\nrounds: 605"
          },
          {
            "name": "benchmarks/bench_delete.py::test_cqlengine_bulk_delete",
            "value": 875.9336891727676,
            "unit": "iter/sec",
            "range": "stddev: 0.00009044238095328107",
            "extra": "mean: 1.141638930390268 msec\nrounds: 589"
          },
          {
            "name": "benchmarks/bench_delete.py::test_coodie_bulk_delete",
            "value": 1027.4649647158224,
            "unit": "iter/sec",
            "range": "stddev: 0.000025337519865816663",
            "extra": "mean: 973.2691958762616 usec\nrounds: 873"
          },
          {
            "name": "benchmarks/bench_insert.py::test_cqlengine_single_insert",
            "value": 1665.870512938106,
            "unit": "iter/sec",
            "range": "stddev: 0.00005551069244460414",
            "extra": "mean: 600.2867523216399 usec\nrounds: 969"
          },
          {
            "name": "benchmarks/bench_insert.py::test_coodie_single_insert",
            "value": 2062.4303886237535,
            "unit": "iter/sec",
            "range": "stddev: 0.000018147798735553254",
            "extra": "mean: 484.86484950762076 usec\nrounds: 1422"
          },
          {
            "name": "benchmarks/bench_insert.py::test_cqlengine_insert_if_not_exists",
            "value": 634.2545638475561,
            "unit": "iter/sec",
            "range": "stddev: 0.0006030628741338271",
            "extra": "mean: 1.5766540077121955 msec\nrounds: 389"
          },
          {
            "name": "benchmarks/bench_insert.py::test_coodie_insert_if_not_exists",
            "value": 819.7354257343737,
            "unit": "iter/sec",
            "range": "stddev: 0.0003257091192206078",
            "extra": "mean: 1.2199057996110552 msec\nrounds: 514"
          },
          {
            "name": "benchmarks/bench_insert.py::test_cqlengine_insert_with_ttl",
            "value": 1648.6230205100212,
            "unit": "iter/sec",
            "range": "stddev: 0.00006408705781645654",
            "extra": "mean: 606.566806091691 usec\nrounds: 985"
          },
          {
            "name": "benchmarks/bench_insert.py::test_coodie_insert_with_ttl",
            "value": 2076.5328387583886,
            "unit": "iter/sec",
            "range": "stddev: 0.000020257363188741566",
            "extra": "mean: 481.5719652177161 usec\nrounds: 805"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_get_by_pk",
            "value": 1499.9339392563454,
            "unit": "iter/sec",
            "range": "stddev: 0.00007703485277620556",
            "extra": "mean: 666.6960282902802 usec\nrounds: 813"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_get_by_pk",
            "value": 2077.088536031619,
            "unit": "iter/sec",
            "range": "stddev: 0.00001859537944318009",
            "extra": "mean: 481.4431270756277 usec\nrounds: 1385"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_filter_secondary_index",
            "value": 216.34282269021145,
            "unit": "iter/sec",
            "range": "stddev: 0.0005747717649088208",
            "extra": "mean: 4.62229339325915 msec\nrounds: 178"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_filter_secondary_index",
            "value": 545.1533617936511,
            "unit": "iter/sec",
            "range": "stddev: 0.0000722570708480782",
            "extra": "mean: 1.8343462043594907 msec\nrounds: 367"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_filter_limit",
            "value": 882.8645064129466,
            "unit": "iter/sec",
            "range": "stddev: 0.00010927957513002223",
            "extra": "mean: 1.132676636942821 msec\nrounds: 628"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_filter_limit",
            "value": 1446.485196597224,
            "unit": "iter/sec",
            "range": "stddev: 0.00006042651020856651",
            "extra": "mean: 691.3309602838966 usec\nrounds: 705"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_count",
            "value": 962.407504329961,
            "unit": "iter/sec",
            "range": "stddev: 0.00006203186858130848",
            "extra": "mean: 1.0390608920866753 msec\nrounds: 556"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_count",
            "value": 1075.1012107327122,
            "unit": "iter/sec",
            "range": "stddev: 0.0000511926305259447",
            "extra": "mean: 930.1449854367398 usec\nrounds: 618"
          },
          {
            "name": "benchmarks/bench_schema.py::test_cqlengine_sync_table_create",
            "value": 5691.486060296954,
            "unit": "iter/sec",
            "range": "stddev: 0.00006968809170068177",
            "extra": "mean: 175.70103649657798 usec\nrounds: 137"
          },
          {
            "name": "benchmarks/bench_schema.py::test_coodie_sync_table_create",
            "value": 43825.722043197,
            "unit": "iter/sec",
            "range": "stddev: 0.0000060361745537561855",
            "extra": "mean: 22.817650306236732 usec\nrounds: 163"
          },
          {
            "name": "benchmarks/bench_schema.py::test_cqlengine_sync_table_noop",
            "value": 4755.050947714756,
            "unit": "iter/sec",
            "range": "stddev: 0.00005596765281146965",
            "extra": "mean: 210.30268886616093 usec\nrounds: 2928"
          },
          {
            "name": "benchmarks/bench_schema.py::test_coodie_sync_table_noop",
            "value": 50593.91519864071,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027553708541686894",
            "extra": "mean: 19.765222676952796 usec\nrounds: 9772"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_cqlengine_model_instantiation",
            "value": 70305.9749443463,
            "unit": "iter/sec",
            "range": "stddev: 0.00018741572783390482",
            "extra": "mean: 14.22354217819457 usec\nrounds: 21587"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 509330.6777011856,
            "unit": "iter/sec",
            "range": "stddev: 3.9111472506230023e-7",
            "extra": "mean: 1.9633610221819007 usec\nrounds: 35610"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_cqlengine_model_serialization",
            "value": 219224.78284560257,
            "unit": "iter/sec",
            "range": "stddev: 9.253411731938769e-7",
            "extra": "mean: 4.561528067309289 usec\nrounds: 43360"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 507155.4354865108,
            "unit": "iter/sec",
            "range": "stddev: 4.130901358904534e-7",
            "extra": "mean: 1.9717820810511608 usec\nrounds: 34031"
          },
          {
            "name": "benchmarks/bench_update.py::test_cqlengine_partial_update",
            "value": 1790.9387189719573,
            "unit": "iter/sec",
            "range": "stddev: 0.0003016995300243855",
            "extra": "mean: 558.3663971339145 usec\nrounds: 977"
          },
          {
            "name": "benchmarks/bench_update.py::test_coodie_partial_update",
            "value": 1048.3741212283262,
            "unit": "iter/sec",
            "range": "stddev: 0.000023926996968018047",
            "extra": "mean: 953.8579594356557 usec\nrounds: 567"
          },
          {
            "name": "benchmarks/bench_update.py::test_cqlengine_update_if_condition",
            "value": 675.13852860033,
            "unit": "iter/sec",
            "range": "stddev: 0.0003587449107104839",
            "extra": "mean: 1.481177503042464 msec\nrounds: 493"
          },
          {
            "name": "benchmarks/bench_update.py::test_coodie_update_if_condition",
            "value": 580.1922362696001,
            "unit": "iter/sec",
            "range": "stddev: 0.0003069909612793882",
            "extra": "mean: 1.723566668919241 msec\nrounds: 444"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "340979+fruch@users.noreply.github.com",
            "name": "fruch",
            "username": "fruch"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "a88b4e34b923dcd59c75d6c4efc8aba84149f594",
          "message": "perf: Phase 4 — optimize `_clone()` and add `LazyDocument`\n\n✗ Show commit stats\n  2>/dev/null | head -40\n  Permission denied and could not request permission from user\n\nImplement two Phase 4 performance optimizations:\n\n- Task 3.10: optimise `_clone()` by using `object.__new__()` and direct slot/dict copy, bypassing Pydantic model construction overhead on internal document copies.\n- Task 7.4: add `LazyDocument` (`src/coodie/lazy.py`) — a thin wrapper that defers `model_validate` until a field is first accessed. Exposed via `QuerySet.all(lazy=True)` on both the sync and async query paths.\n\nUpdate `src/coodie/__init__.py` to export `LazyDocument`. Add unit tests for lazy loading behaviour (`tests/test_lazy.py`) and for the updated `_clone()` and `lazy=True` query option (`tests/test_query.py`). Document results and design rationale in `docs/plans/performance-improvement.md`.\n\nCo-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>",
          "timestamp": "2026-02-25T23:04:44+02:00",
          "tree_id": "a9340c6a008a360a78bb74473d38da6051a7a18c",
          "url": "https://github.com/fruch/coodie/commit/a88b4e34b923dcd59c75d6c4efc8aba84149f594"
        },
        "date": 1772053551726,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_get_or_create_user",
            "value": 1357.6869263361746,
            "unit": "iter/sec",
            "range": "stddev: 0.00022343866242860672",
            "extra": "mean: 736.5468287291967 usec\nrounds: 543"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_get_or_create_user",
            "value": 2048.9126931973965,
            "unit": "iter/sec",
            "range": "stddev: 0.00009760457659041153",
            "extra": "mean: 488.06374391651934 usec\nrounds: 863"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_filter_runs_by_status",
            "value": 1020.720453561398,
            "unit": "iter/sec",
            "range": "stddev: 0.00012121436540311049",
            "extra": "mean: 979.7001681615155 usec\nrounds: 892"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_filter_runs_by_status",
            "value": 1928.7155360902395,
            "unit": "iter/sec",
            "range": "stddev: 0.00012057395859399722",
            "extra": "mean: 518.4797764563725 usec\nrounds: 841"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_latest_runs",
            "value": 1014.2190305282799,
            "unit": "iter/sec",
            "range": "stddev: 0.0014682124974036476",
            "extra": "mean: 985.9803157895059 usec\nrounds: 608"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_latest_runs",
            "value": 2043.2268707300357,
            "unit": "iter/sec",
            "range": "stddev: 0.000025207311353699897",
            "extra": "mean: 489.421911156985 usec\nrounds: 968"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_list_mutation",
            "value": 1359.6552383877165,
            "unit": "iter/sec",
            "range": "stddev: 0.00008834461671783864",
            "extra": "mean: 735.4805628416533 usec\nrounds: 549"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_list_mutation",
            "value": 1011.8513250611259,
            "unit": "iter/sec",
            "range": "stddev: 0.00012266302393605378",
            "extra": "mean: 988.2874837759293 usec\nrounds: 1017"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_batch_events",
            "value": 356.0174362189625,
            "unit": "iter/sec",
            "range": "stddev: 0.00019702692604399628",
            "extra": "mean: 2.80885119172918 msec\nrounds: 266"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_batch_events",
            "value": 849.69435338829,
            "unit": "iter/sec",
            "range": "stddev: 0.000052528129177082214",
            "extra": "mean: 1.1768937807016637 msec\nrounds: 456"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_notification_feed",
            "value": 775.0312628083104,
            "unit": "iter/sec",
            "range": "stddev: 0.000126000064406181",
            "extra": "mean: 1.290270532283459 msec\nrounds: 635"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_notification_feed",
            "value": 1635.3732136521135,
            "unit": "iter/sec",
            "range": "stddev: 0.00011148993992564968",
            "extra": "mean: 611.4812152064062 usec\nrounds: 776"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_status_update",
            "value": 1164.2679657620204,
            "unit": "iter/sec",
            "range": "stddev: 0.00009558970396868568",
            "extra": "mean: 858.90879883953 usec\nrounds: 517"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_status_update",
            "value": 1031.2665000956094,
            "unit": "iter/sec",
            "range": "stddev: 0.00003217979060013405",
            "extra": "mean: 969.6814547037932 usec\nrounds: 574"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_comment_with_collections",
            "value": 1273.3508863547586,
            "unit": "iter/sec",
            "range": "stddev: 0.00008685563858451848",
            "extra": "mean: 785.3294882942404 usec\nrounds: 598"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_comment_with_collections",
            "value": 2063.596300249296,
            "unit": "iter/sec",
            "range": "stddev: 0.000028547088983019994",
            "extra": "mean: 484.590905633623 usec\nrounds: 710"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_multi_model_lookup",
            "value": 730.1448957249091,
            "unit": "iter/sec",
            "range": "stddev: 0.00013379195103815328",
            "extra": "mean: 1.3695911672534133 msec\nrounds: 568"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_multi_model_lookup",
            "value": 1043.1600134860769,
            "unit": "iter/sec",
            "range": "stddev: 0.000038520189723020243",
            "extra": "mean: 958.6257017829481 usec\nrounds: 617"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_argus_model_instantiation",
            "value": 24283.71128334932,
            "unit": "iter/sec",
            "range": "stddev: 0.000026375853343172475",
            "extra": "mean: 41.17986696233178 usec\nrounds: 10373"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 40075.1886014114,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016787597272715605",
            "extra": "mean: 24.95309529160347 usec\nrounds: 15143"
          },
          {
            "name": "benchmarks/bench_batch.py::test_cqlengine_batch_insert_10",
            "value": 649.4608452289893,
            "unit": "iter/sec",
            "range": "stddev: 0.00012200474355697621",
            "extra": "mean: 1.5397387037973262 msec\nrounds: 395"
          },
          {
            "name": "benchmarks/bench_batch.py::test_coodie_batch_insert_10",
            "value": 1743.694465017479,
            "unit": "iter/sec",
            "range": "stddev: 0.00017586553822571423",
            "extra": "mean: 573.4949671873712 usec\nrounds: 640"
          },
          {
            "name": "benchmarks/bench_batch.py::test_cqlengine_batch_insert_100",
            "value": 19.272344105938355,
            "unit": "iter/sec",
            "range": "stddev: 0.00030528281031457605",
            "extra": "mean: 51.88782405000083 msec\nrounds: 20"
          },
          {
            "name": "benchmarks/bench_batch.py::test_coodie_batch_insert_100",
            "value": 472.3486960848544,
            "unit": "iter/sec",
            "range": "stddev: 0.00021852475967956591",
            "extra": "mean: 2.1170800476187965 msec\nrounds: 231"
          },
          {
            "name": "benchmarks/bench_collections.py::test_cqlengine_collection_write",
            "value": 1511.3826137669967,
            "unit": "iter/sec",
            "range": "stddev: 0.00007528643884594912",
            "extra": "mean: 661.6458273974599 usec\nrounds: 730"
          },
          {
            "name": "benchmarks/bench_collections.py::test_coodie_collection_write",
            "value": 2051.1965587509217,
            "unit": "iter/sec",
            "range": "stddev: 0.000026157992733913507",
            "extra": "mean: 487.52031868118536 usec\nrounds: 728"
          },
          {
            "name": "benchmarks/bench_collections.py::test_cqlengine_collection_read",
            "value": 1523.4203175481468,
            "unit": "iter/sec",
            "range": "stddev: 0.00008135185840831279",
            "extra": "mean: 656.4176599728169 usec\nrounds: 747"
          },
          {
            "name": "benchmarks/bench_collections.py::test_coodie_collection_read",
            "value": 2082.4590556663957,
            "unit": "iter/sec",
            "range": "stddev: 0.0000227109946056871",
            "extra": "mean: 480.20151814221185 usec\nrounds: 689"
          },
          {
            "name": "benchmarks/bench_collections.py::test_cqlengine_collection_roundtrip",
            "value": 723.4075311522071,
            "unit": "iter/sec",
            "range": "stddev: 0.0001250910705749784",
            "extra": "mean: 1.3823466814165597 msec\nrounds: 452"
          },
          {
            "name": "benchmarks/bench_collections.py::test_coodie_collection_roundtrip",
            "value": 938.0557433078276,
            "unit": "iter/sec",
            "range": "stddev: 0.00035229162554581054",
            "extra": "mean: 1.0660347288890755 msec\nrounds: 675"
          },
          {
            "name": "benchmarks/bench_delete.py::test_cqlengine_single_delete",
            "value": 914.9762766051686,
            "unit": "iter/sec",
            "range": "stddev: 0.00010227706966430411",
            "extra": "mean: 1.0929245113439385 msec\nrounds: 573"
          },
          {
            "name": "benchmarks/bench_delete.py::test_coodie_single_delete",
            "value": 1002.5505709230561,
            "unit": "iter/sec",
            "range": "stddev: 0.00002536151617713178",
            "extra": "mean: 997.4559179386754 usec\nrounds: 524"
          },
          {
            "name": "benchmarks/bench_delete.py::test_cqlengine_bulk_delete",
            "value": 867.8485674300047,
            "unit": "iter/sec",
            "range": "stddev: 0.00009738479510351217",
            "extra": "mean: 1.1522747602860495 msec\nrounds: 559"
          },
          {
            "name": "benchmarks/bench_delete.py::test_coodie_bulk_delete",
            "value": 1036.6588061465015,
            "unit": "iter/sec",
            "range": "stddev: 0.000034114175611156915",
            "extra": "mean: 964.6375394400297 usec\nrounds: 786"
          },
          {
            "name": "benchmarks/bench_insert.py::test_cqlengine_single_insert",
            "value": 1631.457480908006,
            "unit": "iter/sec",
            "range": "stddev: 0.00006973387377836622",
            "extra": "mean: 612.9488581237428 usec\nrounds: 874"
          },
          {
            "name": "benchmarks/bench_insert.py::test_coodie_single_insert",
            "value": 2080.9646690782756,
            "unit": "iter/sec",
            "range": "stddev: 0.000020043943630474426",
            "extra": "mean: 480.54636143482975 usec\nrounds: 1115"
          },
          {
            "name": "benchmarks/bench_insert.py::test_cqlengine_insert_if_not_exists",
            "value": 771.836989458034,
            "unit": "iter/sec",
            "range": "stddev: 0.00048109309698958074",
            "extra": "mean: 1.295610360294052 msec\nrounds: 408"
          },
          {
            "name": "benchmarks/bench_insert.py::test_coodie_insert_if_not_exists",
            "value": 980.1707417203914,
            "unit": "iter/sec",
            "range": "stddev: 0.00011373458490438478",
            "extra": "mean: 1.020230412351224 msec\nrounds: 502"
          },
          {
            "name": "benchmarks/bench_insert.py::test_cqlengine_insert_with_ttl",
            "value": 1635.8019949680452,
            "unit": "iter/sec",
            "range": "stddev: 0.00006755504075677247",
            "extra": "mean: 611.3209319197185 usec\nrounds: 896"
          },
          {
            "name": "benchmarks/bench_insert.py::test_coodie_insert_with_ttl",
            "value": 2129.398251252165,
            "unit": "iter/sec",
            "range": "stddev: 0.00001722320395741032",
            "extra": "mean: 469.6162398987427 usec\nrounds: 792"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_get_by_pk",
            "value": 1514.7410175373232,
            "unit": "iter/sec",
            "range": "stddev: 0.00007080644512592912",
            "extra": "mean: 660.1788612193305 usec\nrounds: 771"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_get_by_pk",
            "value": 2089.708382467883,
            "unit": "iter/sec",
            "range": "stddev: 0.000022260815538921782",
            "extra": "mean: 478.5356695650663 usec\nrounds: 1150"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_filter_secondary_index",
            "value": 226.50199746173857,
            "unit": "iter/sec",
            "range": "stddev: 0.0006037663891972824",
            "extra": "mean: 4.414972102702641 msec\nrounds: 185"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_filter_secondary_index",
            "value": 535.9475045850394,
            "unit": "iter/sec",
            "range": "stddev: 0.000039876438169445194",
            "extra": "mean: 1.865854382089634 msec\nrounds: 335"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_filter_limit",
            "value": 907.4717161607974,
            "unit": "iter/sec",
            "range": "stddev: 0.00013212907240492543",
            "extra": "mean: 1.1019627192687151 msec\nrounds: 602"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_filter_limit",
            "value": 1751.1231028300354,
            "unit": "iter/sec",
            "range": "stddev: 0.00008978812176202465",
            "extra": "mean: 571.0620791787134 usec\nrounds: 682"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_count",
            "value": 941.1510062506435,
            "unit": "iter/sec",
            "range": "stddev: 0.00007782515431127338",
            "extra": "mean: 1.0625287476276513 msec\nrounds: 527"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_count",
            "value": 1079.615581627903,
            "unit": "iter/sec",
            "range": "stddev: 0.00004488584329388903",
            "extra": "mean: 926.2556200718644 usec\nrounds: 558"
          },
          {
            "name": "benchmarks/bench_schema.py::test_cqlengine_sync_table_create",
            "value": 7276.616514030792,
            "unit": "iter/sec",
            "range": "stddev: 0.000045434394496144945",
            "extra": "mean: 137.42650833279413 usec\nrounds: 120"
          },
          {
            "name": "benchmarks/bench_schema.py::test_coodie_sync_table_create",
            "value": 45416.1524198799,
            "unit": "iter/sec",
            "range": "stddev: 0.000013529404909814193",
            "extra": "mean: 22.018597937465803 usec\nrounds: 194"
          },
          {
            "name": "benchmarks/bench_schema.py::test_cqlengine_sync_table_noop",
            "value": 5347.546509598344,
            "unit": "iter/sec",
            "range": "stddev: 0.0005345589505988135",
            "extra": "mean: 187.00164612034584 usec\nrounds: 2758"
          },
          {
            "name": "benchmarks/bench_schema.py::test_coodie_sync_table_noop",
            "value": 55928.5846477058,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028592564085527095",
            "extra": "mean: 17.87994468837359 usec\nrounds: 7973"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_cqlengine_model_instantiation",
            "value": 75011.51522534371,
            "unit": "iter/sec",
            "range": "stddev: 0.00001932568526379283",
            "extra": "mean: 13.33128649642496 usec\nrounds: 18447"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 479893.7345208995,
            "unit": "iter/sec",
            "range": "stddev: 5.11982353493206e-7",
            "extra": "mean: 2.0837946571616466 usec\nrounds: 30695"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_cqlengine_model_serialization",
            "value": 214534.30075155286,
            "unit": "iter/sec",
            "range": "stddev: 0.000006957787082158277",
            "extra": "mean: 4.661259278804449 usec\nrounds: 43621"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 509835.83251901687,
            "unit": "iter/sec",
            "range": "stddev: 4.713292746330481e-7",
            "extra": "mean: 1.9614156875933197 usec\nrounds: 32599"
          },
          {
            "name": "benchmarks/bench_update.py::test_cqlengine_partial_update",
            "value": 1874.5743127685091,
            "unit": "iter/sec",
            "range": "stddev: 0.00006716970411021835",
            "extra": "mean: 533.4544451978148 usec\nrounds: 885"
          },
          {
            "name": "benchmarks/bench_update.py::test_coodie_partial_update",
            "value": 1060.6816329363576,
            "unit": "iter/sec",
            "range": "stddev: 0.000018612385999335574",
            "extra": "mean: 942.7899653844589 usec\nrounds: 520"
          },
          {
            "name": "benchmarks/bench_update.py::test_cqlengine_update_if_condition",
            "value": 780.1657449381697,
            "unit": "iter/sec",
            "range": "stddev: 0.00014509831712859435",
            "extra": "mean: 1.281778912350545 msec\nrounds: 502"
          },
          {
            "name": "benchmarks/bench_update.py::test_coodie_update_if_condition",
            "value": 655.1255156714147,
            "unit": "iter/sec",
            "range": "stddev: 0.00011300756323528262",
            "extra": "mean: 1.5264250530299308 msec\nrounds: 396"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "0762c5fd136143acc7194e97691c5ab1a7cd5ca4",
          "message": "fix(demos): use coodie[scylla] dependency to include cassandra driver\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-02-25T23:11:32+02:00",
          "tree_id": "99157c511bd69da72a30d075349064661799f2de",
          "url": "https://github.com/fruch/coodie/commit/0762c5fd136143acc7194e97691c5ab1a7cd5ca4"
        },
        "date": 1772053964703,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_get_or_create_user",
            "value": 1227.6133482740242,
            "unit": "iter/sec",
            "range": "stddev: 0.00030012617808525017",
            "extra": "mean: 814.5887313835095 usec\nrounds: 376"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_get_or_create_user",
            "value": 1987.4455616544167,
            "unit": "iter/sec",
            "range": "stddev: 0.00010194496866579819",
            "extra": "mean: 503.1584357800303 usec\nrounds: 872"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_filter_runs_by_status",
            "value": 876.5925413989413,
            "unit": "iter/sec",
            "range": "stddev: 0.00014808244751851816",
            "extra": "mean: 1.1407808677040696 msec\nrounds: 771"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_filter_runs_by_status",
            "value": 1987.0449056367845,
            "unit": "iter/sec",
            "range": "stddev: 0.00004971933324980277",
            "extra": "mean: 503.259889680013 usec\nrounds: 843"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_latest_runs",
            "value": 985.3834569877042,
            "unit": "iter/sec",
            "range": "stddev: 0.0008957645521805023",
            "extra": "mean: 1.0148333553893611 msec\nrounds: 937"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_latest_runs",
            "value": 2065.3018826494877,
            "unit": "iter/sec",
            "range": "stddev: 0.000023517497867649666",
            "extra": "mean: 484.1907172994694 usec\nrounds: 948"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_list_mutation",
            "value": 1286.293006069849,
            "unit": "iter/sec",
            "range": "stddev: 0.00010409515799564521",
            "extra": "mean: 777.4278451963357 usec\nrounds: 562"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_list_mutation",
            "value": 1017.5999622746167,
            "unit": "iter/sec",
            "range": "stddev: 0.00005075741097953519",
            "extra": "mean: 982.7044389474269 usec\nrounds: 950"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_batch_events",
            "value": 308.3854448922114,
            "unit": "iter/sec",
            "range": "stddev: 0.00020652069685366775",
            "extra": "mean: 3.242695193832918 msec\nrounds: 227"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_batch_events",
            "value": 836.880322302297,
            "unit": "iter/sec",
            "range": "stddev: 0.00008933189484506842",
            "extra": "mean: 1.1949139839361418 msec\nrounds: 498"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_notification_feed",
            "value": 689.2105314243444,
            "unit": "iter/sec",
            "range": "stddev: 0.00015345195760141527",
            "extra": "mean: 1.4509354607994283 msec\nrounds: 625"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_notification_feed",
            "value": 1403.3412805059156,
            "unit": "iter/sec",
            "range": "stddev: 0.00003104461840276592",
            "extra": "mean: 712.5850382164288 usec\nrounds: 785"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_status_update",
            "value": 1103.5776485610422,
            "unit": "iter/sec",
            "range": "stddev: 0.00010478304002378663",
            "extra": "mean: 906.1437600733419 usec\nrounds: 546"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_status_update",
            "value": 1011.5987181322542,
            "unit": "iter/sec",
            "range": "stddev: 0.000028846601664772242",
            "extra": "mean: 988.5342696423446 usec\nrounds: 560"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_comment_with_collections",
            "value": 1242.945968671134,
            "unit": "iter/sec",
            "range": "stddev: 0.00008786667779452962",
            "extra": "mean: 804.5402014289696 usec\nrounds: 700"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_comment_with_collections",
            "value": 2004.2590252003354,
            "unit": "iter/sec",
            "range": "stddev: 0.000033770262710298804",
            "extra": "mean: 498.9375062936514 usec\nrounds: 715"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_multi_model_lookup",
            "value": 689.56352571929,
            "unit": "iter/sec",
            "range": "stddev: 0.00014997328214982214",
            "extra": "mean: 1.4501927127843528 msec\nrounds: 571"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_multi_model_lookup",
            "value": 1031.9805743125746,
            "unit": "iter/sec",
            "range": "stddev: 0.000029754411064767843",
            "extra": "mean: 969.0104880764081 usec\nrounds: 629"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_argus_model_instantiation",
            "value": 26900.52168065196,
            "unit": "iter/sec",
            "range": "stddev: 0.000026498822665995885",
            "extra": "mean: 37.17400026183299 usec\nrounds: 11460"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 46970.280661604935,
            "unit": "iter/sec",
            "range": "stddev: 0.000002183075303395178",
            "extra": "mean: 21.29005800932829 usec\nrounds: 18135"
          },
          {
            "name": "benchmarks/bench_batch.py::test_cqlengine_batch_insert_10",
            "value": 569.6954282873767,
            "unit": "iter/sec",
            "range": "stddev: 0.00011195739239916846",
            "extra": "mean: 1.7553238982559656 msec\nrounds: 344"
          },
          {
            "name": "benchmarks/bench_batch.py::test_coodie_batch_insert_10",
            "value": 1634.0924661618697,
            "unit": "iter/sec",
            "range": "stddev: 0.0001555884223621702",
            "extra": "mean: 611.960473906831 usec\nrounds: 709"
          },
          {
            "name": "benchmarks/bench_batch.py::test_cqlengine_batch_insert_100",
            "value": 18.654665925021558,
            "unit": "iter/sec",
            "range": "stddev: 0.0004076626296295137",
            "extra": "mean: 53.605891631578196 msec\nrounds: 19"
          },
          {
            "name": "benchmarks/bench_batch.py::test_coodie_batch_insert_100",
            "value": 471.8017546342825,
            "unit": "iter/sec",
            "range": "stddev: 0.0003394476292116363",
            "extra": "mean: 2.119534296296017 msec\nrounds: 243"
          },
          {
            "name": "benchmarks/bench_collections.py::test_cqlengine_collection_write",
            "value": 1476.3503410830065,
            "unit": "iter/sec",
            "range": "stddev: 0.00005649863729019912",
            "extra": "mean: 677.3460012658173 usec\nrounds: 790"
          },
          {
            "name": "benchmarks/bench_collections.py::test_coodie_collection_write",
            "value": 2025.9089771014317,
            "unit": "iter/sec",
            "range": "stddev: 0.00004006453194436497",
            "extra": "mean: 493.6055920097405 usec\nrounds: 826"
          },
          {
            "name": "benchmarks/bench_collections.py::test_cqlengine_collection_read",
            "value": 1425.4919902935071,
            "unit": "iter/sec",
            "range": "stddev: 0.00007479520111902678",
            "extra": "mean: 701.5121844312162 usec\nrounds: 835"
          },
          {
            "name": "benchmarks/bench_collections.py::test_coodie_collection_read",
            "value": 2097.032647794827,
            "unit": "iter/sec",
            "range": "stddev: 0.000020196824385892075",
            "extra": "mean: 476.8642972972158 usec\nrounds: 814"
          },
          {
            "name": "benchmarks/bench_collections.py::test_cqlengine_collection_roundtrip",
            "value": 720.5822201399636,
            "unit": "iter/sec",
            "range": "stddev: 0.00012203219273597722",
            "extra": "mean: 1.387766686507701 msec\nrounds: 504"
          },
          {
            "name": "benchmarks/bench_collections.py::test_coodie_collection_roundtrip",
            "value": 1029.2004095105149,
            "unit": "iter/sec",
            "range": "stddev: 0.000037509624876545774",
            "extra": "mean: 971.6280626778971 usec\nrounds: 702"
          },
          {
            "name": "benchmarks/bench_delete.py::test_cqlengine_single_delete",
            "value": 882.4826541682534,
            "unit": "iter/sec",
            "range": "stddev: 0.00011692394877271002",
            "extra": "mean: 1.1331667486909505 msec\nrounds: 573"
          },
          {
            "name": "benchmarks/bench_delete.py::test_coodie_single_delete",
            "value": 1027.7654243603517,
            "unit": "iter/sec",
            "range": "stddev: 0.000028027752153489788",
            "extra": "mean: 972.9846678023519 usec\nrounds: 587"
          },
          {
            "name": "benchmarks/bench_delete.py::test_cqlengine_bulk_delete",
            "value": 825.0318542972149,
            "unit": "iter/sec",
            "range": "stddev: 0.00011998952667228729",
            "extra": "mean: 1.2120744123896015 msec\nrounds: 565"
          },
          {
            "name": "benchmarks/bench_delete.py::test_coodie_bulk_delete",
            "value": 1026.886187771441,
            "unit": "iter/sec",
            "range": "stddev: 0.00002889075211802282",
            "extra": "mean: 973.8177530366928 usec\nrounds: 741"
          },
          {
            "name": "benchmarks/bench_insert.py::test_cqlengine_single_insert",
            "value": 1575.2567366674557,
            "unit": "iter/sec",
            "range": "stddev: 0.0000784850525850522",
            "extra": "mean: 634.817155021699 usec\nrounds: 916"
          },
          {
            "name": "benchmarks/bench_insert.py::test_coodie_single_insert",
            "value": 2076.496727682801,
            "unit": "iter/sec",
            "range": "stddev: 0.000019838097713652262",
            "extra": "mean: 481.5803399391423 usec\nrounds: 1312"
          },
          {
            "name": "benchmarks/bench_insert.py::test_cqlengine_insert_if_not_exists",
            "value": 696.1315607713663,
            "unit": "iter/sec",
            "range": "stddev: 0.000671652652562178",
            "extra": "mean: 1.4365100741761005 msec\nrounds: 364"
          },
          {
            "name": "benchmarks/bench_insert.py::test_coodie_insert_if_not_exists",
            "value": 806.0056516460608,
            "unit": "iter/sec",
            "range": "stddev: 0.00046935368025887884",
            "extra": "mean: 1.2406860894309553 msec\nrounds: 492"
          },
          {
            "name": "benchmarks/bench_insert.py::test_cqlengine_insert_with_ttl",
            "value": 1572.2342377658113,
            "unit": "iter/sec",
            "range": "stddev: 0.00008505367132435112",
            "extra": "mean: 636.0375419765872 usec\nrounds: 941"
          },
          {
            "name": "benchmarks/bench_insert.py::test_coodie_insert_with_ttl",
            "value": 2053.357562053779,
            "unit": "iter/sec",
            "range": "stddev: 0.000021032096798570906",
            "extra": "mean: 487.00724047291345 usec\nrounds: 761"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_get_by_pk",
            "value": 1441.8592121559448,
            "unit": "iter/sec",
            "range": "stddev: 0.0000993014751235393",
            "extra": "mean: 693.548989782953 usec\nrounds: 783"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_get_by_pk",
            "value": 2066.794636804169,
            "unit": "iter/sec",
            "range": "stddev: 0.000021447146773140394",
            "extra": "mean: 483.8410078063073 usec\nrounds: 1281"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_filter_secondary_index",
            "value": 185.58927022528053,
            "unit": "iter/sec",
            "range": "stddev: 0.0029579132032556787",
            "extra": "mean: 5.388242535714127 msec\nrounds: 168"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_filter_secondary_index",
            "value": 531.6183068572215,
            "unit": "iter/sec",
            "range": "stddev: 0.00007390503152217943",
            "extra": "mean: 1.881048841059895 msec\nrounds: 302"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_filter_limit",
            "value": 830.7681118825377,
            "unit": "iter/sec",
            "range": "stddev: 0.00020789922470786123",
            "extra": "mean: 1.2037053248637326 msec\nrounds: 551"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_filter_limit",
            "value": 1461.5585029913702,
            "unit": "iter/sec",
            "range": "stddev: 0.00009276325828631233",
            "extra": "mean: 684.2011441576243 usec\nrounds: 659"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_count",
            "value": 934.3486318026978,
            "unit": "iter/sec",
            "range": "stddev: 0.00008310073498929401",
            "extra": "mean: 1.0702643167257995 msec\nrounds: 562"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_count",
            "value": 1064.0487684218526,
            "unit": "iter/sec",
            "range": "stddev: 0.00004765102274173249",
            "extra": "mean: 939.80654804305 usec\nrounds: 562"
          },
          {
            "name": "benchmarks/bench_schema.py::test_cqlengine_sync_table_create",
            "value": 5239.586870392958,
            "unit": "iter/sec",
            "range": "stddev: 0.00009831768902191941",
            "extra": "mean: 190.85474193598054 usec\nrounds: 124"
          },
          {
            "name": "benchmarks/bench_schema.py::test_coodie_sync_table_create",
            "value": 40705.85616052948,
            "unit": "iter/sec",
            "range": "stddev: 0.000006189052581930142",
            "extra": "mean: 24.566489795874926 usec\nrounds: 147"
          },
          {
            "name": "benchmarks/bench_schema.py::test_cqlengine_sync_table_noop",
            "value": 4481.862457770538,
            "unit": "iter/sec",
            "range": "stddev: 0.00006776856754596941",
            "extra": "mean: 223.12152803043423 usec\nrounds: 2087"
          },
          {
            "name": "benchmarks/bench_schema.py::test_coodie_sync_table_noop",
            "value": 48759.41354787901,
            "unit": "iter/sec",
            "range": "stddev: 0.0000029013782410776446",
            "extra": "mean: 20.508860284343985 usec\nrounds: 9777"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_cqlengine_model_instantiation",
            "value": 81164.15568101524,
            "unit": "iter/sec",
            "range": "stddev: 0.000020821938642666274",
            "extra": "mean: 12.320709697641883 usec\nrounds: 19180"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 487782.6901184812,
            "unit": "iter/sec",
            "range": "stddev: 8.997233618672645e-7",
            "extra": "mean: 2.0500932490185386 usec\nrounds: 35121"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_cqlengine_model_serialization",
            "value": 220162.7350125381,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011818909950581197",
            "extra": "mean: 4.542094737072788 usec\nrounds: 43341"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 503200.9992266186,
            "unit": "iter/sec",
            "range": "stddev: 5.337680831271944e-7",
            "extra": "mean: 1.9872774528208876 usec\nrounds: 34359"
          },
          {
            "name": "benchmarks/bench_update.py::test_cqlengine_partial_update",
            "value": 1760.0344400173656,
            "unit": "iter/sec",
            "range": "stddev: 0.00009413552893458579",
            "extra": "mean: 568.1707001086487 usec\nrounds: 917"
          },
          {
            "name": "benchmarks/bench_update.py::test_coodie_partial_update",
            "value": 1022.2763671958219,
            "unit": "iter/sec",
            "range": "stddev: 0.00002523763954379477",
            "extra": "mean: 978.2090558770055 usec\nrounds: 519"
          },
          {
            "name": "benchmarks/bench_update.py::test_cqlengine_update_if_condition",
            "value": 734.379984646995,
            "unit": "iter/sec",
            "range": "stddev: 0.00027891969281712667",
            "extra": "mean: 1.361692885026931 msec\nrounds: 374"
          },
          {
            "name": "benchmarks/bench_update.py::test_coodie_update_if_condition",
            "value": 604.5368971367241,
            "unit": "iter/sec",
            "range": "stddev: 0.0001250094794514495",
            "extra": "mean: 1.6541587531485884 msec\nrounds: 397"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "83d82bbacb45d37d6a6d9aad92c17b9bc9a94ad0",
          "message": "feat(test): add pytest-bats plugin to run .bats files as pytest items\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-02-25T23:29:00+02:00",
          "tree_id": "386203bbc9e60efdda7adf7a48760cec2aa982d8",
          "url": "https://github.com/fruch/coodie/commit/83d82bbacb45d37d6a6d9aad92c17b9bc9a94ad0"
        },
        "date": 1772055012677,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_get_or_create_user",
            "value": 1323.3501829850632,
            "unit": "iter/sec",
            "range": "stddev: 0.00022375752127106038",
            "extra": "mean: 755.657884706158 usec\nrounds: 425"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_get_or_create_user",
            "value": 2076.4296256728167,
            "unit": "iter/sec",
            "range": "stddev: 0.00002089876764147733",
            "extra": "mean: 481.5959027149664 usec\nrounds: 884"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_filter_runs_by_status",
            "value": 889.1936611925026,
            "unit": "iter/sec",
            "range": "stddev: 0.00016750915534252957",
            "extra": "mean: 1.1246144047618314 msec\nrounds: 840"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_filter_runs_by_status",
            "value": 2032.501942895123,
            "unit": "iter/sec",
            "range": "stddev: 0.00004468968973960166",
            "extra": "mean: 492.00444973527885 usec\nrounds: 945"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_latest_runs",
            "value": 999.224650492989,
            "unit": "iter/sec",
            "range": "stddev: 0.0010475547463736847",
            "extra": "mean: 1.0007759511403451 msec\nrounds: 921"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_latest_runs",
            "value": 2067.080236939478,
            "unit": "iter/sec",
            "range": "stddev: 0.000022000661151417545",
            "extra": "mean: 483.7741574466415 usec\nrounds: 940"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_list_mutation",
            "value": 1269.1814846386596,
            "unit": "iter/sec",
            "range": "stddev: 0.00009676341133590176",
            "extra": "mean: 787.9093826244269 usec\nrounds: 541"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_list_mutation",
            "value": 1025.5384392662131,
            "unit": "iter/sec",
            "range": "stddev: 0.00002994062048844516",
            "extra": "mean: 975.0975309277669 usec\nrounds: 970"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_batch_events",
            "value": 323.46800132122866,
            "unit": "iter/sec",
            "range": "stddev: 0.00017001428254340858",
            "extra": "mean: 3.0914959004149623 msec\nrounds: 241"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_batch_events",
            "value": 831.7947833858744,
            "unit": "iter/sec",
            "range": "stddev: 0.00006212419912878336",
            "extra": "mean: 1.2022196099011768 msec\nrounds: 505"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_notification_feed",
            "value": 698.5078492700518,
            "unit": "iter/sec",
            "range": "stddev: 0.0001716084972826835",
            "extra": "mean: 1.4316231393033172 msec\nrounds: 603"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_notification_feed",
            "value": 1429.2739498973299,
            "unit": "iter/sec",
            "range": "stddev: 0.00002673957687522406",
            "extra": "mean: 699.655933750023 usec\nrounds: 800"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_status_update",
            "value": 1129.2378289427636,
            "unit": "iter/sec",
            "range": "stddev: 0.00011052097341603645",
            "extra": "mean: 885.5530468158677 usec\nrounds: 534"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_status_update",
            "value": 1022.7641918586698,
            "unit": "iter/sec",
            "range": "stddev: 0.00001916175707243574",
            "extra": "mean: 977.7424825391076 usec\nrounds: 630"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_comment_with_collections",
            "value": 1261.2901432961246,
            "unit": "iter/sec",
            "range": "stddev: 0.00008351143474631637",
            "extra": "mean: 792.8389873774038 usec\nrounds: 713"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_comment_with_collections",
            "value": 2000.2796073913264,
            "unit": "iter/sec",
            "range": "stddev: 0.000025940162233488226",
            "extra": "mean: 499.930107923339 usec\nrounds: 732"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_multi_model_lookup",
            "value": 683.7483476912906,
            "unit": "iter/sec",
            "range": "stddev: 0.00013672361841292197",
            "extra": "mean: 1.4625263861719713 msec\nrounds: 593"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_multi_model_lookup",
            "value": 1037.201381743769,
            "unit": "iter/sec",
            "range": "stddev: 0.000022794442580599657",
            "extra": "mean: 964.1329230768812 usec\nrounds: 741"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_argus_model_instantiation",
            "value": 26808.637299814927,
            "unit": "iter/sec",
            "range": "stddev: 0.000026235431814990597",
            "extra": "mean: 37.30141106451925 usec\nrounds: 10249"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 46558.97963734197,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021936354541755723",
            "extra": "mean: 21.478133923664515 usec\nrounds: 18182"
          },
          {
            "name": "benchmarks/bench_batch.py::test_cqlengine_batch_insert_10",
            "value": 572.8368807204635,
            "unit": "iter/sec",
            "range": "stddev: 0.00012510439325859768",
            "extra": "mean: 1.745697656097646 msec\nrounds: 410"
          },
          {
            "name": "benchmarks/bench_batch.py::test_coodie_batch_insert_10",
            "value": 1675.442900919506,
            "unit": "iter/sec",
            "range": "stddev: 0.00018775187913101636",
            "extra": "mean: 596.8571053368553 usec\nrounds: 712"
          },
          {
            "name": "benchmarks/bench_batch.py::test_cqlengine_batch_insert_100",
            "value": 18.412250474177824,
            "unit": "iter/sec",
            "range": "stddev: 0.0006818871241250253",
            "extra": "mean: 54.31166610526211 msec\nrounds: 19"
          },
          {
            "name": "benchmarks/bench_batch.py::test_coodie_batch_insert_100",
            "value": 478.1832689101221,
            "unit": "iter/sec",
            "range": "stddev: 0.00029689578673150214",
            "extra": "mean: 2.0912484083334943 msec\nrounds: 240"
          },
          {
            "name": "benchmarks/bench_collections.py::test_cqlengine_collection_write",
            "value": 1276.8857209554412,
            "unit": "iter/sec",
            "range": "stddev: 0.0002903937850474397",
            "extra": "mean: 783.1554410771708 usec\nrounds: 594"
          },
          {
            "name": "benchmarks/bench_collections.py::test_coodie_collection_write",
            "value": 2023.2878312537016,
            "unit": "iter/sec",
            "range": "stddev: 0.00002229584513760675",
            "extra": "mean: 494.2450523118918 usec\nrounds: 822"
          },
          {
            "name": "benchmarks/bench_collections.py::test_cqlengine_collection_read",
            "value": 1430.1417875232346,
            "unit": "iter/sec",
            "range": "stddev: 0.00010279206291868503",
            "extra": "mean: 699.2313690321797 usec\nrounds: 775"
          },
          {
            "name": "benchmarks/bench_collections.py::test_coodie_collection_read",
            "value": 2057.7259299825237,
            "unit": "iter/sec",
            "range": "stddev: 0.00001804713848906404",
            "extra": "mean: 485.97336770135036 usec\nrounds: 805"
          },
          {
            "name": "benchmarks/bench_collections.py::test_cqlengine_collection_roundtrip",
            "value": 726.7590592559031,
            "unit": "iter/sec",
            "range": "stddev: 0.00010326944470520673",
            "extra": "mean: 1.3759718399986047 msec\nrounds: 350"
          },
          {
            "name": "benchmarks/bench_collections.py::test_coodie_collection_roundtrip",
            "value": 1026.055206763809,
            "unit": "iter/sec",
            "range": "stddev: 0.00002171521016378951",
            "extra": "mean: 974.6064280049925 usec\nrounds: 757"
          },
          {
            "name": "benchmarks/bench_delete.py::test_cqlengine_single_delete",
            "value": 886.0471554222379,
            "unit": "iter/sec",
            "range": "stddev: 0.00011627343941399072",
            "extra": "mean: 1.1286081038468647 msec\nrounds: 520"
          },
          {
            "name": "benchmarks/bench_delete.py::test_coodie_single_delete",
            "value": 1043.1975288250214,
            "unit": "iter/sec",
            "range": "stddev: 0.00002209994304557448",
            "extra": "mean: 958.5912278054609 usec\nrounds: 597"
          },
          {
            "name": "benchmarks/bench_delete.py::test_cqlengine_bulk_delete",
            "value": 823.492003733332,
            "unit": "iter/sec",
            "range": "stddev: 0.00010285414450412428",
            "extra": "mean: 1.2143408745518625 msec\nrounds: 558"
          },
          {
            "name": "benchmarks/bench_delete.py::test_coodie_bulk_delete",
            "value": 1038.1320563776637,
            "unit": "iter/sec",
            "range": "stddev: 0.000022214194681604416",
            "extra": "mean: 963.2685878993881 usec\nrounds: 876"
          },
          {
            "name": "benchmarks/bench_insert.py::test_cqlengine_single_insert",
            "value": 1629.6703775477717,
            "unit": "iter/sec",
            "range": "stddev: 0.0000628374670258811",
            "extra": "mean: 613.6210204082736 usec\nrounds: 980"
          },
          {
            "name": "benchmarks/bench_insert.py::test_coodie_single_insert",
            "value": 2093.744470030625,
            "unit": "iter/sec",
            "range": "stddev: 0.000020210756381289746",
            "extra": "mean: 477.6132017606585 usec\nrounds: 1363"
          },
          {
            "name": "benchmarks/bench_insert.py::test_cqlengine_insert_if_not_exists",
            "value": 723.0062925726343,
            "unit": "iter/sec",
            "range": "stddev: 0.000253777152937916",
            "extra": "mean: 1.3831138266331735 msec\nrounds: 398"
          },
          {
            "name": "benchmarks/bench_insert.py::test_coodie_insert_if_not_exists",
            "value": 889.7700460201806,
            "unit": "iter/sec",
            "range": "stddev: 0.00022338710848267897",
            "extra": "mean: 1.1238858899250013 msec\nrounds: 536"
          },
          {
            "name": "benchmarks/bench_insert.py::test_cqlengine_insert_with_ttl",
            "value": 1584.3298619835273,
            "unit": "iter/sec",
            "range": "stddev: 0.0000973360125222928",
            "extra": "mean: 631.1816901235668 usec\nrounds: 810"
          },
          {
            "name": "benchmarks/bench_insert.py::test_coodie_insert_with_ttl",
            "value": 2085.6954659678436,
            "unit": "iter/sec",
            "range": "stddev: 0.00002086933169030323",
            "extra": "mean: 479.4563810090853 usec\nrounds: 832"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_get_by_pk",
            "value": 1434.664206863578,
            "unit": "iter/sec",
            "range": "stddev: 0.00008098913018430242",
            "extra": "mean: 697.0272173905917 usec\nrounds: 828"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_get_by_pk",
            "value": 2076.3599893091955,
            "unit": "iter/sec",
            "range": "stddev: 0.000019894667137301023",
            "extra": "mean: 481.61205433971963 usec\nrounds: 1325"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_filter_secondary_index",
            "value": 178.0388306362241,
            "unit": "iter/sec",
            "range": "stddev: 0.0025809053490746803",
            "extra": "mean: 5.616752235602126 msec\nrounds: 191"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_filter_secondary_index",
            "value": 517.2097607234006,
            "unit": "iter/sec",
            "range": "stddev: 0.000237825072375041",
            "extra": "mean: 1.9334515238098755 msec\nrounds: 231"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_filter_limit",
            "value": 800.1810740362286,
            "unit": "iter/sec",
            "range": "stddev: 0.00017901993531406547",
            "extra": "mean: 1.249717135842586 msec\nrounds: 611"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_filter_limit",
            "value": 1474.7060132379368,
            "unit": "iter/sec",
            "range": "stddev: 0.00008187848500077345",
            "extra": "mean: 678.101256130604 usec\nrounds: 734"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_count",
            "value": 940.0218190294975,
            "unit": "iter/sec",
            "range": "stddev: 0.00008076585716555376",
            "extra": "mean: 1.0638050944736852 msec\nrounds: 561"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_count",
            "value": 1071.725098240099,
            "unit": "iter/sec",
            "range": "stddev: 0.00004250516685494087",
            "extra": "mean: 933.0750970021322 usec\nrounds: 567"
          },
          {
            "name": "benchmarks/bench_schema.py::test_cqlengine_sync_table_create",
            "value": 5504.320952205927,
            "unit": "iter/sec",
            "range": "stddev: 0.00007629864964580528",
            "extra": "mean: 181.67545255500357 usec\nrounds: 137"
          },
          {
            "name": "benchmarks/bench_schema.py::test_coodie_sync_table_create",
            "value": 44252.935303964696,
            "unit": "iter/sec",
            "range": "stddev: 0.000006848301024024597",
            "extra": "mean: 22.59737106999111 usec\nrounds: 159"
          },
          {
            "name": "benchmarks/bench_schema.py::test_cqlengine_sync_table_noop",
            "value": 4372.105529509446,
            "unit": "iter/sec",
            "range": "stddev: 0.00007355464642765959",
            "extra": "mean: 228.72275000009 usec\nrounds: 2184"
          },
          {
            "name": "benchmarks/bench_schema.py::test_coodie_sync_table_noop",
            "value": 47409.58661207348,
            "unit": "iter/sec",
            "range": "stddev: 0.00000364203124622012",
            "extra": "mean: 21.092780415540194 usec\nrounds: 9773"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_cqlengine_model_instantiation",
            "value": 81172.85629293168,
            "unit": "iter/sec",
            "range": "stddev: 0.00001788337005440032",
            "extra": "mean: 12.3193890872986 usec\nrounds: 21278"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 498321.0349235319,
            "unit": "iter/sec",
            "range": "stddev: 6.561834648976426e-7",
            "extra": "mean: 2.0067384876768277 usec\nrounds: 37134"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_cqlengine_model_serialization",
            "value": 217190.89042338528,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012323393446772414",
            "extra": "mean: 4.604244671821321 usec\nrounds: 45044"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 496586.4549152858,
            "unit": "iter/sec",
            "range": "stddev: 0.000006037701031208958",
            "extra": "mean: 2.0137480394437923 usec\nrounds: 22825"
          },
          {
            "name": "benchmarks/bench_update.py::test_cqlengine_partial_update",
            "value": 1787.402658787739,
            "unit": "iter/sec",
            "range": "stddev: 0.00009645603403019058",
            "extra": "mean: 559.4710263428973 usec\nrounds: 949"
          },
          {
            "name": "benchmarks/bench_update.py::test_coodie_partial_update",
            "value": 1033.6458599456064,
            "unit": "iter/sec",
            "range": "stddev: 0.000042348810120247776",
            "extra": "mean: 967.4493351645825 usec\nrounds: 546"
          },
          {
            "name": "benchmarks/bench_update.py::test_cqlengine_update_if_condition",
            "value": 733.319383835063,
            "unit": "iter/sec",
            "range": "stddev: 0.0003105527730066217",
            "extra": "mean: 1.3636623032794648 msec\nrounds: 488"
          },
          {
            "name": "benchmarks/bench_update.py::test_coodie_update_if_condition",
            "value": 601.9050122886198,
            "unit": "iter/sec",
            "range": "stddev: 0.0003496150439575123",
            "extra": "mean: 1.6613917139478636 msec\nrounds: 423"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "e64b66ec71c30985bc914d253e991ccdcf1515f0",
          "message": "docs: complete Phase 4 — API reference, recipes, and integration examples\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-02-25T23:29:46+02:00",
          "tree_id": "0c36a480362c43fcda32c9f9cc7c717daf69de8e",
          "url": "https://github.com/fruch/coodie/commit/e64b66ec71c30985bc914d253e991ccdcf1515f0"
        },
        "date": 1772055054229,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_get_or_create_user",
            "value": 1343.8798111830888,
            "unit": "iter/sec",
            "range": "stddev: 0.0002864230121989948",
            "extra": "mean: 744.1141623518006 usec\nrounds: 425"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_get_or_create_user",
            "value": 2074.0513979849065,
            "unit": "iter/sec",
            "range": "stddev: 0.00002250640541771477",
            "extra": "mean: 482.14812852351366 usec\nrounds: 887"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_filter_runs_by_status",
            "value": 895.5721724709862,
            "unit": "iter/sec",
            "range": "stddev: 0.0007948289499697518",
            "extra": "mean: 1.1166045917225023 msec\nrounds: 894"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_filter_runs_by_status",
            "value": 2107.3395385465624,
            "unit": "iter/sec",
            "range": "stddev: 0.000020953507126267812",
            "extra": "mean: 474.5319782163356 usec\nrounds: 964"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_latest_runs",
            "value": 1071.532365857252,
            "unit": "iter/sec",
            "range": "stddev: 0.00008498157790296716",
            "extra": "mean: 933.2429256114682 usec\nrounds: 941"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_latest_runs",
            "value": 2063.082533423545,
            "unit": "iter/sec",
            "range": "stddev: 0.000032235526669297874",
            "extra": "mean: 484.71158269202544 usec\nrounds: 1040"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_list_mutation",
            "value": 1317.9232059986193,
            "unit": "iter/sec",
            "range": "stddev: 0.0000977362826879377",
            "extra": "mean: 758.7695515553792 usec\nrounds: 611"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_list_mutation",
            "value": 1037.4682141584929,
            "unit": "iter/sec",
            "range": "stddev: 0.000025146110044486953",
            "extra": "mean: 963.8849521872978 usec\nrounds: 983"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_batch_events",
            "value": 331.09526977436735,
            "unit": "iter/sec",
            "range": "stddev: 0.0001302004985088377",
            "extra": "mean: 3.020278727272285 msec\nrounds: 253"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_batch_events",
            "value": 853.1481032917425,
            "unit": "iter/sec",
            "range": "stddev: 0.00006259635260027532",
            "extra": "mean: 1.1721294299801543 msec\nrounds: 507"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_notification_feed",
            "value": 735.6827417327058,
            "unit": "iter/sec",
            "range": "stddev: 0.00012248414408172554",
            "extra": "mean: 1.3592815805965013 msec\nrounds: 670"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_notification_feed",
            "value": 1431.9407085040157,
            "unit": "iter/sec",
            "range": "stddev: 0.00004799561777623466",
            "extra": "mean: 698.352937423453 usec\nrounds: 815"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_status_update",
            "value": 1141.5486775471234,
            "unit": "iter/sec",
            "range": "stddev: 0.0000903400892770135",
            "extra": "mean: 876.0029420284794 usec\nrounds: 621"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_status_update",
            "value": 1031.9870257949694,
            "unit": "iter/sec",
            "range": "stddev: 0.00003151208121638974",
            "extra": "mean: 969.0044302927851 usec\nrounds: 581"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_comment_with_collections",
            "value": 1297.539805050683,
            "unit": "iter/sec",
            "range": "stddev: 0.00006800654959139439",
            "extra": "mean: 770.689266030601 usec\nrounds: 733"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_comment_with_collections",
            "value": 2013.57418658865,
            "unit": "iter/sec",
            "range": "stddev: 0.000029207122127098287",
            "extra": "mean: 496.6293304018645 usec\nrounds: 796"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_multi_model_lookup",
            "value": 732.9308115209764,
            "unit": "iter/sec",
            "range": "stddev: 0.00012592852178386072",
            "extra": "mean: 1.3643852656771276 msec\nrounds: 606"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_multi_model_lookup",
            "value": 1026.8727768361148,
            "unit": "iter/sec",
            "range": "stddev: 0.000028839138944767614",
            "extra": "mean: 973.8304710746037 usec\nrounds: 726"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_argus_model_instantiation",
            "value": 26749.023832450614,
            "unit": "iter/sec",
            "range": "stddev: 0.000025858895261088565",
            "extra": "mean: 37.38454181594652 usec\nrounds: 11168"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 46412.12819552581,
            "unit": "iter/sec",
            "range": "stddev: 0.000002040111921621631",
            "extra": "mean: 21.54609234437996 usec\nrounds: 17543"
          },
          {
            "name": "benchmarks/bench_batch.py::test_cqlengine_batch_insert_10",
            "value": 584.5298770760418,
            "unit": "iter/sec",
            "range": "stddev: 0.00010949028864983557",
            "extra": "mean: 1.7107765389208829 msec\nrounds: 334"
          },
          {
            "name": "benchmarks/bench_batch.py::test_coodie_batch_insert_10",
            "value": 1638.2153275687206,
            "unit": "iter/sec",
            "range": "stddev: 0.00017316353676435502",
            "extra": "mean: 610.4203660968686 usec\nrounds: 702"
          },
          {
            "name": "benchmarks/bench_batch.py::test_cqlengine_batch_insert_100",
            "value": 18.69365396945684,
            "unit": "iter/sec",
            "range": "stddev: 0.0007569037088753795",
            "extra": "mean: 53.49408957894902 msec\nrounds: 19"
          },
          {
            "name": "benchmarks/bench_batch.py::test_coodie_batch_insert_100",
            "value": 498.36565187579134,
            "unit": "iter/sec",
            "range": "stddev: 0.0002998065011210316",
            "extra": "mean: 2.006558831324178 msec\nrounds: 249"
          },
          {
            "name": "benchmarks/bench_collections.py::test_cqlengine_collection_write",
            "value": 1387.8408290767595,
            "unit": "iter/sec",
            "range": "stddev: 0.00023727068712696553",
            "extra": "mean: 720.543724502784 usec\nrounds: 755"
          },
          {
            "name": "benchmarks/bench_collections.py::test_coodie_collection_write",
            "value": 2100.2785151971707,
            "unit": "iter/sec",
            "range": "stddev: 0.0000208251278334254",
            "extra": "mean: 476.12732919191984 usec\nrounds: 805"
          },
          {
            "name": "benchmarks/bench_collections.py::test_cqlengine_collection_read",
            "value": 1477.055287907963,
            "unit": "iter/sec",
            "range": "stddev: 0.00007648686081887813",
            "extra": "mean: 677.0227277114025 usec\nrounds: 830"
          },
          {
            "name": "benchmarks/bench_collections.py::test_coodie_collection_read",
            "value": 2084.5673041181294,
            "unit": "iter/sec",
            "range": "stddev: 0.000022926569654297045",
            "extra": "mean: 479.71586142815727 usec\nrounds: 700"
          },
          {
            "name": "benchmarks/bench_collections.py::test_cqlengine_collection_roundtrip",
            "value": 757.9151560045023,
            "unit": "iter/sec",
            "range": "stddev: 0.0001008244791017175",
            "extra": "mean: 1.319408896995404 msec\nrounds: 466"
          },
          {
            "name": "benchmarks/bench_collections.py::test_coodie_collection_roundtrip",
            "value": 1048.794115622361,
            "unit": "iter/sec",
            "range": "stddev: 0.000021561679809506213",
            "extra": "mean: 953.4759826589927 usec\nrounds: 692"
          },
          {
            "name": "benchmarks/bench_delete.py::test_cqlengine_single_delete",
            "value": 898.3370375190862,
            "unit": "iter/sec",
            "range": "stddev: 0.0001026970039670461",
            "extra": "mean: 1.1131679517096098 msec\nrounds: 497"
          },
          {
            "name": "benchmarks/bench_delete.py::test_coodie_single_delete",
            "value": 1036.8425134112035,
            "unit": "iter/sec",
            "range": "stddev: 0.000025947920534000406",
            "extra": "mean: 964.4666254183658 usec\nrounds: 598"
          },
          {
            "name": "benchmarks/bench_delete.py::test_cqlengine_bulk_delete",
            "value": 857.3551798004281,
            "unit": "iter/sec",
            "range": "stddev: 0.00010066482839436043",
            "extra": "mean: 1.1663777435073948 msec\nrounds: 616"
          },
          {
            "name": "benchmarks/bench_delete.py::test_coodie_bulk_delete",
            "value": 1029.126654581198,
            "unit": "iter/sec",
            "range": "stddev: 0.000027316624868666227",
            "extra": "mean: 971.6976968271696 usec\nrounds: 851"
          },
          {
            "name": "benchmarks/bench_insert.py::test_cqlengine_single_insert",
            "value": 1656.475963641939,
            "unit": "iter/sec",
            "range": "stddev: 0.000057096171918290635",
            "extra": "mean: 603.6912227820037 usec\nrounds: 992"
          },
          {
            "name": "benchmarks/bench_insert.py::test_coodie_single_insert",
            "value": 2071.6081808652034,
            "unit": "iter/sec",
            "range": "stddev: 0.000020306979536460487",
            "extra": "mean: 482.7167652824927 usec\nrounds: 1325"
          },
          {
            "name": "benchmarks/bench_insert.py::test_cqlengine_insert_if_not_exists",
            "value": 470.9035305560739,
            "unit": "iter/sec",
            "range": "stddev: 0.0011647386142032076",
            "extra": "mean: 2.1235771981134524 msec\nrounds: 424"
          },
          {
            "name": "benchmarks/bench_insert.py::test_coodie_insert_if_not_exists",
            "value": 610.8208009056927,
            "unit": "iter/sec",
            "range": "stddev: 0.0009655784136704076",
            "extra": "mean: 1.6371413653845006 msec\nrounds: 416"
          },
          {
            "name": "benchmarks/bench_insert.py::test_cqlengine_insert_with_ttl",
            "value": 1651.5608528148723,
            "unit": "iter/sec",
            "range": "stddev: 0.00005729130788182616",
            "extra": "mean: 605.4878318868051 usec\nrounds: 922"
          },
          {
            "name": "benchmarks/bench_insert.py::test_coodie_insert_with_ttl",
            "value": 2073.273264796371,
            "unit": "iter/sec",
            "range": "stddev: 0.000025056242768996483",
            "extra": "mean: 482.32908656072215 usec\nrounds: 878"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_get_by_pk",
            "value": 1465.7573365303106,
            "unit": "iter/sec",
            "range": "stddev: 0.00007660213953918508",
            "extra": "mean: 682.2411698563726 usec\nrounds: 836"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_get_by_pk",
            "value": 2095.8724128786357,
            "unit": "iter/sec",
            "range": "stddev: 0.000020165961471051193",
            "extra": "mean: 477.1282802594465 usec\nrounds: 1388"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_filter_secondary_index",
            "value": 209.99200845585537,
            "unit": "iter/sec",
            "range": "stddev: 0.0021754422029016504",
            "extra": "mean: 4.762085982954064 msec\nrounds: 176"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_filter_secondary_index",
            "value": 542.7428901567743,
            "unit": "iter/sec",
            "range": "stddev: 0.00007279960815008768",
            "extra": "mean: 1.8424930443789775 msec\nrounds: 338"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_filter_limit",
            "value": 860.7847566397994,
            "unit": "iter/sec",
            "range": "stddev: 0.0001370480614585263",
            "extra": "mean: 1.161730609523858 msec\nrounds: 630"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_filter_limit",
            "value": 1558.9609355904815,
            "unit": "iter/sec",
            "range": "stddev: 0.00009874166100551068",
            "extra": "mean: 641.4528915833506 usec\nrounds: 701"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_count",
            "value": 949.4087464544663,
            "unit": "iter/sec",
            "range": "stddev: 0.00007588868736553351",
            "extra": "mean: 1.0532871155173837 msec\nrounds: 580"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_count",
            "value": 1035.2935340073786,
            "unit": "iter/sec",
            "range": "stddev: 0.00003542522890733522",
            "extra": "mean: 965.9096354337637 usec\nrounds: 587"
          },
          {
            "name": "benchmarks/bench_schema.py::test_cqlengine_sync_table_create",
            "value": 5572.207788940837,
            "unit": "iter/sec",
            "range": "stddev: 0.0000664012961754622",
            "extra": "mean: 179.46208000080333 usec\nrounds: 125"
          },
          {
            "name": "benchmarks/bench_schema.py::test_coodie_sync_table_create",
            "value": 42953.539033143265,
            "unit": "iter/sec",
            "range": "stddev: 0.000006076701997174425",
            "extra": "mean: 23.28096875157115 usec\nrounds: 160"
          },
          {
            "name": "benchmarks/bench_schema.py::test_cqlengine_sync_table_noop",
            "value": 4414.0338270345865,
            "unit": "iter/sec",
            "range": "stddev: 0.00006049455352827054",
            "extra": "mean: 226.55014419583975 usec\nrounds: 2455"
          },
          {
            "name": "benchmarks/bench_schema.py::test_coodie_sync_table_noop",
            "value": 50284.38210251891,
            "unit": "iter/sec",
            "range": "stddev: 0.00001321177932974031",
            "extra": "mean: 19.886890485423837 usec\nrounds: 7378"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_cqlengine_model_instantiation",
            "value": 80984.13270489126,
            "unit": "iter/sec",
            "range": "stddev: 0.000018327588098607735",
            "extra": "mean: 12.348097912513696 usec\nrounds: 21846"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 496060.0989727748,
            "unit": "iter/sec",
            "range": "stddev: 3.9446432593405533e-7",
            "extra": "mean: 2.0158847729756286 usec\nrounds: 34419"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_cqlengine_model_serialization",
            "value": 216139.2865813229,
            "unit": "iter/sec",
            "range": "stddev: 6.863173429064107e-7",
            "extra": "mean: 4.626646158673924 usec\nrounds: 45023"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 506864.11939631443,
            "unit": "iter/sec",
            "range": "stddev: 4.25635903507005e-7",
            "extra": "mean: 1.9729153469987588 usec\nrounds: 36750"
          },
          {
            "name": "benchmarks/bench_update.py::test_cqlengine_partial_update",
            "value": 1892.7421015807447,
            "unit": "iter/sec",
            "range": "stddev: 0.00005887564110636256",
            "extra": "mean: 528.3339970959798 usec\nrounds: 1033"
          },
          {
            "name": "benchmarks/bench_update.py::test_coodie_partial_update",
            "value": 1040.20565377356,
            "unit": "iter/sec",
            "range": "stddev: 0.000026078176394363393",
            "extra": "mean: 961.3483606556975 usec\nrounds: 549"
          },
          {
            "name": "benchmarks/bench_update.py::test_cqlengine_update_if_condition",
            "value": 663.5061482774701,
            "unit": "iter/sec",
            "range": "stddev: 0.0004690138111490678",
            "extra": "mean: 1.5071450394184023 msec\nrounds: 482"
          },
          {
            "name": "benchmarks/bench_update.py::test_coodie_update_if_condition",
            "value": 558.8782979909907,
            "unit": "iter/sec",
            "range": "stddev: 0.0006904546085063323",
            "extra": "mean: 1.789298320573042 msec\nrounds: 418"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "fbc6ef4bc37aef7692b6f02a99f12215ae0f0947",
          "message": "docs(perf): add Phase 5 benchmark results analysis to performance plan\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-02-25T23:59:52+02:00",
          "tree_id": "a5da7b3523a1b4fffbb00e9e10f044792d111ca0",
          "url": "https://github.com/fruch/coodie/commit/fbc6ef4bc37aef7692b6f02a99f12215ae0f0947"
        },
        "date": 1772056881317,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_get_or_create_user",
            "value": 1300.7652434286088,
            "unit": "iter/sec",
            "range": "stddev: 0.00025245802047167904",
            "extra": "mean: 768.7782288556236 usec\nrounds: 402"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_get_or_create_user",
            "value": 2073.3616705894788,
            "unit": "iter/sec",
            "range": "stddev: 0.00001986764675032541",
            "extra": "mean: 482.3085205948123 usec\nrounds: 874"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_filter_runs_by_status",
            "value": 924.4209219296547,
            "unit": "iter/sec",
            "range": "stddev: 0.0001230766830876616",
            "extra": "mean: 1.0817582946008837 msec\nrounds: 852"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_filter_runs_by_status",
            "value": 2044.6405904610688,
            "unit": "iter/sec",
            "range": "stddev: 0.00003463632941905853",
            "extra": "mean: 489.08351162807486 usec\nrounds: 946"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_latest_runs",
            "value": 1012.6655604366235,
            "unit": "iter/sec",
            "range": "stddev: 0.0008372617662268668",
            "extra": "mean: 987.4928496322491 usec\nrounds: 951"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_latest_runs",
            "value": 2073.2396217500573,
            "unit": "iter/sec",
            "range": "stddev: 0.000035374629400195506",
            "extra": "mean: 482.33691345136594 usec\nrounds: 959"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_list_mutation",
            "value": 1312.2895532179086,
            "unit": "iter/sec",
            "range": "stddev: 0.00007199334977106372",
            "extra": "mean: 762.0269456141497 usec\nrounds: 570"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_list_mutation",
            "value": 1014.2790075994332,
            "unit": "iter/sec",
            "range": "stddev: 0.000027786339084837274",
            "extra": "mean: 985.9220120968212 usec\nrounds: 992"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_batch_events",
            "value": 317.801905471236,
            "unit": "iter/sec",
            "range": "stddev: 0.00021292917837326223",
            "extra": "mean: 3.146614236051235 msec\nrounds: 233"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_batch_events",
            "value": 822.9495864550221,
            "unit": "iter/sec",
            "range": "stddev: 0.00010153474030460946",
            "extra": "mean: 1.2151412631576242 msec\nrounds: 494"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_notification_feed",
            "value": 691.8992499574587,
            "unit": "iter/sec",
            "range": "stddev: 0.00017489746845629231",
            "extra": "mean: 1.4452971296926322 msec\nrounds: 586"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_notification_feed",
            "value": 1438.9411905787758,
            "unit": "iter/sec",
            "range": "stddev: 0.000050354446699185324",
            "extra": "mean: 694.955434278573 usec\nrounds: 776"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_status_update",
            "value": 1137.1821816817312,
            "unit": "iter/sec",
            "range": "stddev: 0.00007833749863814956",
            "extra": "mean: 879.3665747744498 usec\nrounds: 555"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_status_update",
            "value": 1032.0647185133355,
            "unit": "iter/sec",
            "range": "stddev: 0.00002568637325001698",
            "extra": "mean: 968.9314846848714 usec\nrounds: 555"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_comment_with_collections",
            "value": 1304.3157551222698,
            "unit": "iter/sec",
            "range": "stddev: 0.00006768730014432501",
            "extra": "mean: 766.6855177305264 usec\nrounds: 705"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_comment_with_collections",
            "value": 2033.010150244343,
            "unit": "iter/sec",
            "range": "stddev: 0.00003119745721435355",
            "extra": "mean: 491.88145955877894 usec\nrounds: 816"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_multi_model_lookup",
            "value": 707.8499652965022,
            "unit": "iter/sec",
            "range": "stddev: 0.00011277148922543352",
            "extra": "mean: 1.4127287547172835 msec\nrounds: 583"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_multi_model_lookup",
            "value": 1047.2739779083793,
            "unit": "iter/sec",
            "range": "stddev: 0.00001598557699305837",
            "extra": "mean: 954.8599708332341 usec\nrounds: 720"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_argus_model_instantiation",
            "value": 27133.466865985836,
            "unit": "iter/sec",
            "range": "stddev: 0.000026322488259021382",
            "extra": "mean: 36.85485547936327 usec\nrounds: 9189"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 47227.36576104264,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020470444306367795",
            "extra": "mean: 21.17416425594691 usec\nrounds: 17698"
          },
          {
            "name": "benchmarks/bench_batch.py::test_cqlengine_batch_insert_10",
            "value": 578.049658417295,
            "unit": "iter/sec",
            "range": "stddev: 0.00009408287957340636",
            "extra": "mean: 1.7299551784841614 msec\nrounds: 409"
          },
          {
            "name": "benchmarks/bench_batch.py::test_coodie_batch_insert_10",
            "value": 1701.6432644917961,
            "unit": "iter/sec",
            "range": "stddev: 0.00017590200077050857",
            "extra": "mean: 587.6672395836472 usec\nrounds: 672"
          },
          {
            "name": "benchmarks/bench_batch.py::test_cqlengine_batch_insert_100",
            "value": 18.580705241385274,
            "unit": "iter/sec",
            "range": "stddev: 0.0006109167394020142",
            "extra": "mean: 53.81927042105348 msec\nrounds: 19"
          },
          {
            "name": "benchmarks/bench_batch.py::test_coodie_batch_insert_100",
            "value": 481.6802503527149,
            "unit": "iter/sec",
            "range": "stddev: 0.0003738685720566896",
            "extra": "mean: 2.076066019455314 msec\nrounds: 257"
          },
          {
            "name": "benchmarks/bench_collections.py::test_cqlengine_collection_write",
            "value": 1388.5838600179966,
            "unit": "iter/sec",
            "range": "stddev: 0.0002462176958242079",
            "extra": "mean: 720.1581617022681 usec\nrounds: 705"
          },
          {
            "name": "benchmarks/bench_collections.py::test_coodie_collection_write",
            "value": 2096.281202114069,
            "unit": "iter/sec",
            "range": "stddev: 0.000015470512084004103",
            "extra": "mean: 477.0352369670227 usec\nrounds: 844"
          },
          {
            "name": "benchmarks/bench_collections.py::test_cqlengine_collection_read",
            "value": 1484.9509044435063,
            "unit": "iter/sec",
            "range": "stddev: 0.00007191736015447881",
            "extra": "mean: 673.4229374234804 usec\nrounds: 815"
          },
          {
            "name": "benchmarks/bench_collections.py::test_coodie_collection_read",
            "value": 2084.059270548718,
            "unit": "iter/sec",
            "range": "stddev: 0.000021182349036063874",
            "extra": "mean: 479.83280232558224 usec\nrounds: 774"
          },
          {
            "name": "benchmarks/bench_collections.py::test_cqlengine_collection_roundtrip",
            "value": 709.2337505122067,
            "unit": "iter/sec",
            "range": "stddev: 0.00011180563386370861",
            "extra": "mean: 1.409972381147686 msec\nrounds: 488"
          },
          {
            "name": "benchmarks/bench_collections.py::test_coodie_collection_roundtrip",
            "value": 1026.5330470745837,
            "unit": "iter/sec",
            "range": "stddev: 0.000023237688088271797",
            "extra": "mean: 974.1527589879375 usec\nrounds: 751"
          },
          {
            "name": "benchmarks/bench_delete.py::test_cqlengine_single_delete",
            "value": 890.9594109862852,
            "unit": "iter/sec",
            "range": "stddev: 0.0000900142430810723",
            "extra": "mean: 1.1223855853242601 msec\nrounds: 586"
          },
          {
            "name": "benchmarks/bench_delete.py::test_coodie_single_delete",
            "value": 1039.6328901689992,
            "unit": "iter/sec",
            "range": "stddev: 0.00002148736610982771",
            "extra": "mean: 961.8779950655883 usec\nrounds: 608"
          },
          {
            "name": "benchmarks/bench_delete.py::test_cqlengine_bulk_delete",
            "value": 842.0270066905059,
            "unit": "iter/sec",
            "range": "stddev: 0.00009371380714784513",
            "extra": "mean: 1.1876103641026783 msec\nrounds: 585"
          },
          {
            "name": "benchmarks/bench_delete.py::test_coodie_bulk_delete",
            "value": 1034.6214061916396,
            "unit": "iter/sec",
            "range": "stddev: 0.0000238130965222995",
            "extra": "mean: 966.5371255761293 usec\nrounds: 868"
          },
          {
            "name": "benchmarks/bench_insert.py::test_cqlengine_single_insert",
            "value": 1616.6005951755947,
            "unit": "iter/sec",
            "range": "stddev: 0.000056779217012414596",
            "extra": "mean: 618.5819818353959 usec\nrounds: 1046"
          },
          {
            "name": "benchmarks/bench_insert.py::test_coodie_single_insert",
            "value": 2083.855326191081,
            "unit": "iter/sec",
            "range": "stddev: 0.000018487316750363264",
            "extra": "mean: 479.8797629717525 usec\nrounds: 1696"
          },
          {
            "name": "benchmarks/bench_insert.py::test_cqlengine_insert_if_not_exists",
            "value": 720.162140687478,
            "unit": "iter/sec",
            "range": "stddev: 0.0001790946228624531",
            "extra": "mean: 1.3885761879198266 msec\nrounds: 447"
          },
          {
            "name": "benchmarks/bench_insert.py::test_coodie_insert_if_not_exists",
            "value": 850.0854667014195,
            "unit": "iter/sec",
            "range": "stddev: 0.0001780927325794782",
            "extra": "mean: 1.1763523071160042 msec\nrounds: 534"
          },
          {
            "name": "benchmarks/bench_insert.py::test_cqlengine_insert_with_ttl",
            "value": 1587.538805114273,
            "unit": "iter/sec",
            "range": "stddev: 0.00006484695922842952",
            "extra": "mean: 629.9058623187601 usec\nrounds: 966"
          },
          {
            "name": "benchmarks/bench_insert.py::test_coodie_insert_with_ttl",
            "value": 2063.908864465144,
            "unit": "iter/sec",
            "range": "stddev: 0.000028148059076458436",
            "extra": "mean: 484.5175178115954 usec\nrounds: 786"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_get_by_pk",
            "value": 1459.2626340442473,
            "unit": "iter/sec",
            "range": "stddev: 0.00007028048002521796",
            "extra": "mean: 685.2776029963626 usec\nrounds: 801"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_get_by_pk",
            "value": 2038.3094303716543,
            "unit": "iter/sec",
            "range": "stddev: 0.00008900376160403868",
            "extra": "mean: 490.6026460455837 usec\nrounds: 1277"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_filter_secondary_index",
            "value": 215.11204256287422,
            "unit": "iter/sec",
            "range": "stddev: 0.0006644743875959784",
            "extra": "mean: 4.648740201087134 msec\nrounds: 184"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_filter_secondary_index",
            "value": 543.651852902538,
            "unit": "iter/sec",
            "range": "stddev: 0.00003222642739993335",
            "extra": "mean: 1.839412474474308 msec\nrounds: 333"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_filter_limit",
            "value": 862.3666812205965,
            "unit": "iter/sec",
            "range": "stddev: 0.00011939924430016557",
            "extra": "mean: 1.1595995320512578 msec\nrounds: 780"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_filter_limit",
            "value": 1510.7353784424818,
            "unit": "iter/sec",
            "range": "stddev: 0.00008553589474361339",
            "extra": "mean: 661.9292923628802 usec\nrounds: 838"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_count",
            "value": 943.3973428473221,
            "unit": "iter/sec",
            "range": "stddev: 0.00007994160178839041",
            "extra": "mean: 1.0599987455782334 msec\nrounds: 735"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_count",
            "value": 1089.1656499262351,
            "unit": "iter/sec",
            "range": "stddev: 0.00003275629865702429",
            "extra": "mean: 918.1339863846478 usec\nrounds: 661"
          },
          {
            "name": "benchmarks/bench_schema.py::test_cqlengine_sync_table_create",
            "value": 5721.877780589413,
            "unit": "iter/sec",
            "range": "stddev: 0.00005725127994827052",
            "extra": "mean: 174.76780147110895 usec\nrounds: 136"
          },
          {
            "name": "benchmarks/bench_schema.py::test_coodie_sync_table_create",
            "value": 43453.60822326657,
            "unit": "iter/sec",
            "range": "stddev: 0.000006373650361478136",
            "extra": "mean: 23.01304864861752 usec\nrounds: 185"
          },
          {
            "name": "benchmarks/bench_schema.py::test_cqlengine_sync_table_noop",
            "value": 4739.848561127511,
            "unit": "iter/sec",
            "range": "stddev: 0.00005656807460911208",
            "extra": "mean: 210.97720467299507 usec\nrounds: 3210"
          },
          {
            "name": "benchmarks/bench_schema.py::test_coodie_sync_table_noop",
            "value": 50272.38091426097,
            "unit": "iter/sec",
            "range": "stddev: 0.00001315917790222376",
            "extra": "mean: 19.891637949383973 usec\nrounds: 10377"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_cqlengine_model_instantiation",
            "value": 82644.41499652599,
            "unit": "iter/sec",
            "range": "stddev: 0.00001761317093630765",
            "extra": "mean: 12.10003120043908 usec\nrounds: 22083"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 502170.9802321392,
            "unit": "iter/sec",
            "range": "stddev: 4.247212704975221e-7",
            "extra": "mean: 1.9913536213058922 usec\nrounds: 35982"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_cqlengine_model_serialization",
            "value": 221837.31104702974,
            "unit": "iter/sec",
            "range": "stddev: 7.192304685553908e-7",
            "extra": "mean: 4.507807975494252 usec\nrounds: 40198"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 508795.3660733279,
            "unit": "iter/sec",
            "range": "stddev: 4.185741015230952e-7",
            "extra": "mean: 1.9654267052736467 usec\nrounds: 34218"
          },
          {
            "name": "benchmarks/bench_update.py::test_cqlengine_partial_update",
            "value": 1712.648460988349,
            "unit": "iter/sec",
            "range": "stddev: 0.0001583305028960138",
            "extra": "mean: 583.890986842047 usec\nrounds: 988"
          },
          {
            "name": "benchmarks/bench_update.py::test_coodie_partial_update",
            "value": 1047.5250672885702,
            "unit": "iter/sec",
            "range": "stddev: 0.000012937633881821163",
            "extra": "mean: 954.6310930662645 usec\nrounds: 548"
          },
          {
            "name": "benchmarks/bench_update.py::test_cqlengine_update_if_condition",
            "value": 744.8493007162571,
            "unit": "iter/sec",
            "range": "stddev: 0.00019727358818082865",
            "extra": "mean: 1.3425534521390927 msec\nrounds: 491"
          },
          {
            "name": "benchmarks/bench_update.py::test_coodie_update_if_condition",
            "value": 600.8831823631511,
            "unit": "iter/sec",
            "range": "stddev: 0.00015413615211016447",
            "extra": "mean: 1.664216988179306 msec\nrounds: 423"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "7576aab81c8036c62cf04177c763326968e892a2",
          "message": "style(demo): apply ruff format to flask-blog app.py\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-02-26T00:01:23+02:00",
          "tree_id": "b3df59395bac31ce77b78aaff951249c11c085a9",
          "url": "https://github.com/fruch/coodie/commit/7576aab81c8036c62cf04177c763326968e892a2"
        },
        "date": 1772056955610,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_get_or_create_user",
            "value": 1331.4684054147413,
            "unit": "iter/sec",
            "range": "stddev: 0.0002686799313469651",
            "extra": "mean: 751.0504912720843 usec\nrounds: 401"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_get_or_create_user",
            "value": 2032.7655673905642,
            "unit": "iter/sec",
            "range": "stddev: 0.00004892388617651468",
            "extra": "mean: 491.9406428571532 usec\nrounds: 784"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_filter_runs_by_status",
            "value": 879.0690396545183,
            "unit": "iter/sec",
            "range": "stddev: 0.00026657958862277555",
            "extra": "mean: 1.137567079365016 msec\nrounds: 819"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_filter_runs_by_status",
            "value": 1998.8886743367764,
            "unit": "iter/sec",
            "range": "stddev: 0.00006237857521531175",
            "extra": "mean: 500.27798588222834 usec\nrounds: 850"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_latest_runs",
            "value": 987.192466028268,
            "unit": "iter/sec",
            "range": "stddev: 0.0009693329961371599",
            "extra": "mean: 1.0129736950113286 msec\nrounds: 882"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_latest_runs",
            "value": 2045.2619709122991,
            "unit": "iter/sec",
            "range": "stddev: 0.00002696857153271457",
            "extra": "mean: 488.93492091575195 usec\nrounds: 961"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_list_mutation",
            "value": 1355.0232609316126,
            "unit": "iter/sec",
            "range": "stddev: 0.00007732929409555744",
            "extra": "mean: 737.9947111110661 usec\nrounds: 630"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_list_mutation",
            "value": 1036.1138287209217,
            "unit": "iter/sec",
            "range": "stddev: 0.00003763680622211121",
            "extra": "mean: 965.1449216101053 usec\nrounds: 944"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_batch_events",
            "value": 328.641044888683,
            "unit": "iter/sec",
            "range": "stddev: 0.00016725234935725626",
            "extra": "mean: 3.0428335582328714 msec\nrounds: 249"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_batch_events",
            "value": 848.9531083806072,
            "unit": "iter/sec",
            "range": "stddev: 0.000050625465722151176",
            "extra": "mean: 1.1779213600001033 msec\nrounds: 450"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_notification_feed",
            "value": 729.2770792756743,
            "unit": "iter/sec",
            "range": "stddev: 0.00012282005761364413",
            "extra": "mean: 1.3712209370315198 msec\nrounds: 667"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_notification_feed",
            "value": 1422.6157543988008,
            "unit": "iter/sec",
            "range": "stddev: 0.00003102999693141566",
            "extra": "mean: 702.9304975064059 usec\nrounds: 802"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_status_update",
            "value": 1150.9383572475742,
            "unit": "iter/sec",
            "range": "stddev: 0.00008378470544549273",
            "extra": "mean: 868.8562629813315 usec\nrounds: 597"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_status_update",
            "value": 1022.2249779679055,
            "unit": "iter/sec",
            "range": "stddev: 0.000023604171763859737",
            "extra": "mean: 978.258232339336 usec\nrounds: 637"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_comment_with_collections",
            "value": 1259.817215829934,
            "unit": "iter/sec",
            "range": "stddev: 0.0000841944853321879",
            "extra": "mean: 793.7659427373571 usec\nrounds: 716"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_comment_with_collections",
            "value": 1985.1261608438554,
            "unit": "iter/sec",
            "range": "stddev: 0.00005096079879289401",
            "extra": "mean: 503.7463208761054 usec\nrounds: 776"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_multi_model_lookup",
            "value": 722.3429474385282,
            "unit": "iter/sec",
            "range": "stddev: 0.00012486494726596855",
            "extra": "mean: 1.3843839737704375 msec\nrounds: 610"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_multi_model_lookup",
            "value": 1031.3791849781915,
            "unit": "iter/sec",
            "range": "stddev: 0.000024482438781926368",
            "extra": "mean: 969.5755106994378 usec\nrounds: 701"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_argus_model_instantiation",
            "value": 27197.630554909338,
            "unit": "iter/sec",
            "range": "stddev: 0.000025211699528803616",
            "extra": "mean: 36.767908806654994 usec\nrounds: 11832"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 47099.62340694963,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019453545642147393",
            "extra": "mean: 21.23159226475786 usec\nrounds: 18073"
          },
          {
            "name": "benchmarks/bench_batch.py::test_cqlengine_batch_insert_10",
            "value": 582.5662737513428,
            "unit": "iter/sec",
            "range": "stddev: 0.0001236920734572167",
            "extra": "mean: 1.7165428983052162 msec\nrounds: 413"
          },
          {
            "name": "benchmarks/bench_batch.py::test_coodie_batch_insert_10",
            "value": 1667.448358950663,
            "unit": "iter/sec",
            "range": "stddev: 0.000169814461674852",
            "extra": "mean: 599.7187227011378 usec\nrounds: 696"
          },
          {
            "name": "benchmarks/bench_batch.py::test_cqlengine_batch_insert_100",
            "value": 18.59709712664575,
            "unit": "iter/sec",
            "range": "stddev: 0.000445728920473004",
            "extra": "mean: 53.77183294736947 msec\nrounds: 19"
          },
          {
            "name": "benchmarks/bench_batch.py::test_coodie_batch_insert_100",
            "value": 483.60627910520446,
            "unit": "iter/sec",
            "range": "stddev: 0.00021648413382346804",
            "extra": "mean: 2.0677978000001493 msec\nrounds: 245"
          },
          {
            "name": "benchmarks/bench_collections.py::test_cqlengine_collection_write",
            "value": 1346.4144596982292,
            "unit": "iter/sec",
            "range": "stddev: 0.0002482904601129783",
            "extra": "mean: 742.71335456701 usec\nrounds: 832"
          },
          {
            "name": "benchmarks/bench_collections.py::test_coodie_collection_write",
            "value": 2025.7974267863415,
            "unit": "iter/sec",
            "range": "stddev: 0.000021256831934886206",
            "extra": "mean: 493.63277234800677 usec\nrounds: 839"
          },
          {
            "name": "benchmarks/bench_collections.py::test_cqlengine_collection_read",
            "value": 1445.7688182921518,
            "unit": "iter/sec",
            "range": "stddev: 0.00008578166097064334",
            "extra": "mean: 691.6735147056729 usec\nrounds: 816"
          },
          {
            "name": "benchmarks/bench_collections.py::test_coodie_collection_read",
            "value": 2096.367428540712,
            "unit": "iter/sec",
            "range": "stddev: 0.000017897493823223295",
            "extra": "mean: 477.0156158627704 usec\nrounds: 643"
          },
          {
            "name": "benchmarks/bench_collections.py::test_cqlengine_collection_roundtrip",
            "value": 726.3868796248764,
            "unit": "iter/sec",
            "range": "stddev: 0.00011957249847537244",
            "extra": "mean: 1.376676848178238 msec\nrounds: 494"
          },
          {
            "name": "benchmarks/bench_collections.py::test_coodie_collection_roundtrip",
            "value": 1030.9672238857875,
            "unit": "iter/sec",
            "range": "stddev: 0.00002467507814625015",
            "extra": "mean: 969.9629404618026 usec\nrounds: 823"
          },
          {
            "name": "benchmarks/bench_delete.py::test_cqlengine_single_delete",
            "value": 884.4090881756591,
            "unit": "iter/sec",
            "range": "stddev: 0.00011564526041482236",
            "extra": "mean: 1.1306984667726327 msec\nrounds: 632"
          },
          {
            "name": "benchmarks/bench_delete.py::test_coodie_single_delete",
            "value": 1034.175376188868,
            "unit": "iter/sec",
            "range": "stddev: 0.000026112563989704426",
            "extra": "mean: 966.9539838447799 usec\nrounds: 619"
          },
          {
            "name": "benchmarks/bench_delete.py::test_cqlengine_bulk_delete",
            "value": 847.889781755189,
            "unit": "iter/sec",
            "range": "stddev: 0.00012331045563285963",
            "extra": "mean: 1.1793985745764415 msec\nrounds: 590"
          },
          {
            "name": "benchmarks/bench_delete.py::test_coodie_bulk_delete",
            "value": 1030.7405254308107,
            "unit": "iter/sec",
            "range": "stddev: 0.000025554943434993203",
            "extra": "mean: 970.1762716490047 usec\nrounds: 843"
          },
          {
            "name": "benchmarks/bench_insert.py::test_cqlengine_single_insert",
            "value": 1634.4519392557502,
            "unit": "iter/sec",
            "range": "stddev: 0.00006785313707875128",
            "extra": "mean: 611.825882414965 usec\nrounds: 944"
          },
          {
            "name": "benchmarks/bench_insert.py::test_coodie_single_insert",
            "value": 2076.887059542531,
            "unit": "iter/sec",
            "range": "stddev: 0.000021773993260761508",
            "extra": "mean: 481.4898313345294 usec\nrounds: 1334"
          },
          {
            "name": "benchmarks/bench_insert.py::test_cqlengine_insert_if_not_exists",
            "value": 732.1629941127558,
            "unit": "iter/sec",
            "range": "stddev: 0.0003219773213470955",
            "extra": "mean: 1.365816092920419 msec\nrounds: 452"
          },
          {
            "name": "benchmarks/bench_insert.py::test_coodie_insert_if_not_exists",
            "value": 862.8285167186355,
            "unit": "iter/sec",
            "range": "stddev: 0.00030131469907923066",
            "extra": "mean: 1.1589788476197243 msec\nrounds: 210"
          },
          {
            "name": "benchmarks/bench_insert.py::test_cqlengine_insert_with_ttl",
            "value": 1616.2164287544638,
            "unit": "iter/sec",
            "range": "stddev: 0.00006913192482288731",
            "extra": "mean: 618.7290156248748 usec\nrounds: 896"
          },
          {
            "name": "benchmarks/bench_insert.py::test_coodie_insert_with_ttl",
            "value": 2034.0832132106004,
            "unit": "iter/sec",
            "range": "stddev: 0.000019860209987965726",
            "extra": "mean: 491.6219717587651 usec\nrounds: 779"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_get_by_pk",
            "value": 1453.7745442151527,
            "unit": "iter/sec",
            "range": "stddev: 0.0000893387653063429",
            "extra": "mean: 687.8645688075854 usec\nrounds: 763"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_get_by_pk",
            "value": 2080.79803105922,
            "unit": "iter/sec",
            "range": "stddev: 0.00002109257993323002",
            "extra": "mean: 480.5848453686564 usec\nrounds: 1371"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_filter_secondary_index",
            "value": 200.04933921543648,
            "unit": "iter/sec",
            "range": "stddev: 0.002375073201858575",
            "extra": "mean: 4.998766823833811 msec\nrounds: 193"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_filter_secondary_index",
            "value": 541.0572710887527,
            "unit": "iter/sec",
            "range": "stddev: 0.00006357593326167574",
            "extra": "mean: 1.8482331786942465 msec\nrounds: 291"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_filter_limit",
            "value": 827.2163780865138,
            "unit": "iter/sec",
            "range": "stddev: 0.00018063279791581406",
            "extra": "mean: 1.2088735504888852 msec\nrounds: 614"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_filter_limit",
            "value": 1445.0089722144057,
            "unit": "iter/sec",
            "range": "stddev: 0.00007935330182881616",
            "extra": "mean: 692.0372255319278 usec\nrounds: 705"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_count",
            "value": 936.8910584767407,
            "unit": "iter/sec",
            "range": "stddev: 0.00011828452020979635",
            "extra": "mean: 1.0673599571180303 msec\nrounds: 583"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_count",
            "value": 1067.2294148644103,
            "unit": "iter/sec",
            "range": "stddev: 0.000042853789490512046",
            "extra": "mean: 937.0056578950725 usec\nrounds: 570"
          },
          {
            "name": "benchmarks/bench_schema.py::test_cqlengine_sync_table_create",
            "value": 5595.473087388084,
            "unit": "iter/sec",
            "range": "stddev: 0.0000587431834277503",
            "extra": "mean: 178.7158984383197 usec\nrounds: 128"
          },
          {
            "name": "benchmarks/bench_schema.py::test_coodie_sync_table_create",
            "value": 44523.96602316897,
            "unit": "iter/sec",
            "range": "stddev: 0.0000058877006470396995",
            "extra": "mean: 22.459814102805424 usec\nrounds: 156"
          },
          {
            "name": "benchmarks/bench_schema.py::test_cqlengine_sync_table_noop",
            "value": 4558.256376464785,
            "unit": "iter/sec",
            "range": "stddev: 0.00007045328812520967",
            "extra": "mean: 219.38213154556328 usec\nrounds: 2349"
          },
          {
            "name": "benchmarks/bench_schema.py::test_coodie_sync_table_noop",
            "value": 49467.741138610625,
            "unit": "iter/sec",
            "range": "stddev: 0.000013668712904643339",
            "extra": "mean: 20.215194326297603 usec\nrounds: 7755"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_cqlengine_model_instantiation",
            "value": 82301.90799364878,
            "unit": "iter/sec",
            "range": "stddev: 0.00001798998118747622",
            "extra": "mean: 12.150386599508359 usec\nrounds: 22059"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 508130.27816251817,
            "unit": "iter/sec",
            "range": "stddev: 4.649476485376127e-7",
            "extra": "mean: 1.9679992375501867 usec\nrounds: 36723"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_cqlengine_model_serialization",
            "value": 221706.4883596607,
            "unit": "iter/sec",
            "range": "stddev: 7.305821925511023e-7",
            "extra": "mean: 4.510467904654924 usec\nrounds: 43511"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 525363.2150853697,
            "unit": "iter/sec",
            "range": "stddev: 4.2479160929948263e-7",
            "extra": "mean: 1.9034450286693625 usec\nrounds: 33472"
          },
          {
            "name": "benchmarks/bench_update.py::test_cqlengine_partial_update",
            "value": 1803.5429874365377,
            "unit": "iter/sec",
            "range": "stddev: 0.0000756312614846938",
            "extra": "mean: 554.4641890800441 usec\nrounds: 989"
          },
          {
            "name": "benchmarks/bench_update.py::test_coodie_partial_update",
            "value": 1043.9679474765014,
            "unit": "iter/sec",
            "range": "stddev: 0.000021088195403930584",
            "extra": "mean: 957.8838147447137 usec\nrounds: 529"
          },
          {
            "name": "benchmarks/bench_update.py::test_cqlengine_update_if_condition",
            "value": 755.6055533311213,
            "unit": "iter/sec",
            "range": "stddev: 0.0003577902999595917",
            "extra": "mean: 1.3234418349513903 msec\nrounds: 515"
          },
          {
            "name": "benchmarks/bench_update.py::test_coodie_update_if_condition",
            "value": 609.6208759851011,
            "unit": "iter/sec",
            "range": "stddev: 0.0003786320590883257",
            "extra": "mean: 1.64036377262192 msec\nrounds: 431"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "4afa28af15b56650e56967bd98ada06fd5117b3f",
          "message": "docs(demos): add CI testing section to demos-extension-plan\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-02-26T12:35:00+02:00",
          "tree_id": "bcfd0a34cee0b3cf9cb9df815424e32c70726be5",
          "url": "https://github.com/fruch/coodie/commit/4afa28af15b56650e56967bd98ada06fd5117b3f"
        },
        "date": 1772102166507,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_get_or_create_user",
            "value": 1319.288448543844,
            "unit": "iter/sec",
            "range": "stddev: 0.00027850116285470434",
            "extra": "mean: 757.9843521738885 usec\nrounds: 460"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_get_or_create_user",
            "value": 2094.3064831887564,
            "unit": "iter/sec",
            "range": "stddev: 0.0000190822101925332",
            "extra": "mean: 477.48503288659856 usec\nrounds: 821"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_filter_runs_by_status",
            "value": 961.7746881983634,
            "unit": "iter/sec",
            "range": "stddev: 0.0001312444593338691",
            "extra": "mean: 1.0397445600000577 msec\nrounds: 800"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_filter_runs_by_status",
            "value": 1999.777870117904,
            "unit": "iter/sec",
            "range": "stddev: 0.00004305011867072331",
            "extra": "mean: 500.0555386389196 usec\nrounds: 867"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_latest_runs",
            "value": 999.2248408384982,
            "unit": "iter/sec",
            "range": "stddev: 0.0012182840437272293",
            "extra": "mean: 1.0007757604993601 msec\nrounds: 881"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_latest_runs",
            "value": 2091.211017131846,
            "unit": "iter/sec",
            "range": "stddev: 0.00003197656359834058",
            "extra": "mean: 478.1918189066965 usec\nrounds: 878"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_list_mutation",
            "value": 1201.0017082625975,
            "unit": "iter/sec",
            "range": "stddev: 0.0002886437456933044",
            "extra": "mean: 832.6382827936422 usec\nrounds: 587"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_list_mutation",
            "value": 1013.3887533486121,
            "unit": "iter/sec",
            "range": "stddev: 0.00011641061669520324",
            "extra": "mean: 986.7881370260222 usec\nrounds: 1029"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_batch_events",
            "value": 362.91623947701265,
            "unit": "iter/sec",
            "range": "stddev: 0.0001626518652320209",
            "extra": "mean: 2.755456745173677 msec\nrounds: 259"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_batch_events",
            "value": 857.9762443537784,
            "unit": "iter/sec",
            "range": "stddev: 0.00005296837606774114",
            "extra": "mean: 1.1655334358973926 msec\nrounds: 468"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_notification_feed",
            "value": 761.3763170120811,
            "unit": "iter/sec",
            "range": "stddev: 0.0001286322441707123",
            "extra": "mean: 1.3134109607248692 msec\nrounds: 662"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_notification_feed",
            "value": 1571.5038081065165,
            "unit": "iter/sec",
            "range": "stddev: 0.00011010384904626834",
            "extra": "mean: 636.3331700766836 usec\nrounds: 782"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_status_update",
            "value": 1193.7334872624283,
            "unit": "iter/sec",
            "range": "stddev: 0.00008772260126993567",
            "extra": "mean: 837.7079228071968 usec\nrounds: 570"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_status_update",
            "value": 1010.6548509596287,
            "unit": "iter/sec",
            "range": "stddev: 0.000028718820672746596",
            "extra": "mean: 989.4574780405876 usec\nrounds: 592"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_comment_with_collections",
            "value": 1272.8018396544994,
            "unit": "iter/sec",
            "range": "stddev: 0.0000775260522866184",
            "extra": "mean: 785.6682547469046 usec\nrounds: 632"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_comment_with_collections",
            "value": 2029.3782306259077,
            "unit": "iter/sec",
            "range": "stddev: 0.00003649934203994657",
            "extra": "mean: 492.7617656032393 usec\nrounds: 721"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_multi_model_lookup",
            "value": 733.4941028888692,
            "unit": "iter/sec",
            "range": "stddev: 0.00011906753913211467",
            "extra": "mean: 1.363337477508676 msec\nrounds: 578"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_multi_model_lookup",
            "value": 1048.5983055539273,
            "unit": "iter/sec",
            "range": "stddev: 0.00002309552774328644",
            "extra": "mean: 953.654030054669 usec\nrounds: 732"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_argus_model_instantiation",
            "value": 23981.255302933856,
            "unit": "iter/sec",
            "range": "stddev: 0.000027224842140277288",
            "extra": "mean: 41.6992349803165 usec\nrounds: 10120"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 40413.52197994708,
            "unit": "iter/sec",
            "range": "stddev: 0.000002038194230483579",
            "extra": "mean: 24.74419330481004 usec\nrounds: 14966"
          },
          {
            "name": "benchmarks/bench_batch.py::test_cqlengine_batch_insert_10",
            "value": 644.3170125550163,
            "unit": "iter/sec",
            "range": "stddev: 0.00014382562800638855",
            "extra": "mean: 1.5520310352112783 msec\nrounds: 426"
          },
          {
            "name": "benchmarks/bench_batch.py::test_coodie_batch_insert_10",
            "value": 1674.484145527433,
            "unit": "iter/sec",
            "range": "stddev: 0.0001832333777905916",
            "extra": "mean: 597.1988463856238 usec\nrounds: 664"
          },
          {
            "name": "benchmarks/bench_batch.py::test_cqlengine_batch_insert_100",
            "value": 19.37655064721856,
            "unit": "iter/sec",
            "range": "stddev: 0.0007147631655053401",
            "extra": "mean: 51.608772800000224 msec\nrounds: 20"
          },
          {
            "name": "benchmarks/bench_batch.py::test_coodie_batch_insert_100",
            "value": 468.4081930359685,
            "unit": "iter/sec",
            "range": "stddev: 0.0002786732163727776",
            "extra": "mean: 2.134890069959155 msec\nrounds: 243"
          },
          {
            "name": "benchmarks/bench_collections.py::test_cqlengine_collection_write",
            "value": 1516.9603563285475,
            "unit": "iter/sec",
            "range": "stddev: 0.00008484965830479943",
            "extra": "mean: 659.2130083216342 usec\nrounds: 721"
          },
          {
            "name": "benchmarks/bench_collections.py::test_coodie_collection_write",
            "value": 2056.2213652100395,
            "unit": "iter/sec",
            "range": "stddev: 0.00001984156059298382",
            "extra": "mean: 486.3289609374581 usec\nrounds: 768"
          },
          {
            "name": "benchmarks/bench_collections.py::test_cqlengine_collection_read",
            "value": 1491.6539086462103,
            "unit": "iter/sec",
            "range": "stddev: 0.0000735735519139473",
            "extra": "mean: 670.3967952643762 usec\nrounds: 718"
          },
          {
            "name": "benchmarks/bench_collections.py::test_coodie_collection_read",
            "value": 2092.389048114826,
            "unit": "iter/sec",
            "range": "stddev: 0.000022430156149196516",
            "extra": "mean: 477.92259326771335 usec\nrounds: 713"
          },
          {
            "name": "benchmarks/bench_collections.py::test_cqlengine_collection_roundtrip",
            "value": 723.5842669686238,
            "unit": "iter/sec",
            "range": "stddev: 0.00011831726376321816",
            "extra": "mean: 1.382009042553384 msec\nrounds: 470"
          },
          {
            "name": "benchmarks/bench_collections.py::test_coodie_collection_roundtrip",
            "value": 1039.7490693062746,
            "unit": "iter/sec",
            "range": "stddev: 0.000052957488104023184",
            "extra": "mean: 961.7705170606256 usec\nrounds: 762"
          },
          {
            "name": "benchmarks/bench_delete.py::test_cqlengine_single_delete",
            "value": 878.9579492378829,
            "unit": "iter/sec",
            "range": "stddev: 0.00022527699642742766",
            "extra": "mean: 1.1377108550722694 msec\nrounds: 552"
          },
          {
            "name": "benchmarks/bench_delete.py::test_coodie_single_delete",
            "value": 1054.8603905088105,
            "unit": "iter/sec",
            "range": "stddev: 0.00002699175287575497",
            "extra": "mean: 947.9927476636518 usec\nrounds: 535"
          },
          {
            "name": "benchmarks/bench_delete.py::test_cqlengine_bulk_delete",
            "value": 869.4116915235526,
            "unit": "iter/sec",
            "range": "stddev: 0.00009382909244491488",
            "extra": "mean: 1.1502030738137476 msec\nrounds: 569"
          },
          {
            "name": "benchmarks/bench_delete.py::test_coodie_bulk_delete",
            "value": 1032.8078833126763,
            "unit": "iter/sec",
            "range": "stddev: 0.00003892583575683934",
            "extra": "mean: 968.2342826359471 usec\nrounds: 789"
          },
          {
            "name": "benchmarks/bench_insert.py::test_cqlengine_single_insert",
            "value": 1626.8117441289041,
            "unit": "iter/sec",
            "range": "stddev: 0.00007212348776063147",
            "extra": "mean: 614.6992751982265 usec\nrounds: 883"
          },
          {
            "name": "benchmarks/bench_insert.py::test_coodie_single_insert",
            "value": 2047.7358522751772,
            "unit": "iter/sec",
            "range": "stddev: 0.000037712668227047644",
            "extra": "mean: 488.34423584903806 usec\nrounds: 1166"
          },
          {
            "name": "benchmarks/bench_insert.py::test_cqlengine_insert_if_not_exists",
            "value": 761.2971814509033,
            "unit": "iter/sec",
            "range": "stddev: 0.00014994677559663981",
            "extra": "mean: 1.3135474875845063 msec\nrounds: 443"
          },
          {
            "name": "benchmarks/bench_insert.py::test_coodie_insert_if_not_exists",
            "value": 840.7085758648581,
            "unit": "iter/sec",
            "range": "stddev: 0.0007662320618046949",
            "extra": "mean: 1.189472819367014 msec\nrounds: 537"
          },
          {
            "name": "benchmarks/bench_insert.py::test_cqlengine_insert_with_ttl",
            "value": 1623.6255854063118,
            "unit": "iter/sec",
            "range": "stddev: 0.00007495554790180805",
            "extra": "mean: 615.9055443498387 usec\nrounds: 823"
          },
          {
            "name": "benchmarks/bench_insert.py::test_coodie_insert_with_ttl",
            "value": 2112.7413740093616,
            "unit": "iter/sec",
            "range": "stddev: 0.000036810853963524516",
            "extra": "mean: 473.31869972437477 usec\nrounds: 726"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_get_by_pk",
            "value": 1434.8983367484516,
            "unit": "iter/sec",
            "range": "stddev: 0.00016811366616856032",
            "extra": "mean: 696.9134846626472 usec\nrounds: 489"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_get_by_pk",
            "value": 2075.40954639835,
            "unit": "iter/sec",
            "range": "stddev: 0.000026034774271510935",
            "extra": "mean: 481.8326106938231 usec\nrounds: 1066"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_filter_secondary_index",
            "value": 222.73973695821874,
            "unit": "iter/sec",
            "range": "stddev: 0.000659321833869914",
            "extra": "mean: 4.489544675127181 msec\nrounds: 197"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_filter_secondary_index",
            "value": 528.9439060924799,
            "unit": "iter/sec",
            "range": "stddev: 0.000026107655110486105",
            "extra": "mean: 1.890559638709896 msec\nrounds: 310"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_filter_limit",
            "value": 885.3246733666812,
            "unit": "iter/sec",
            "range": "stddev: 0.00012078035602620818",
            "extra": "mean: 1.1295291208785987 msec\nrounds: 546"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_filter_limit",
            "value": 1485.8635067754758,
            "unit": "iter/sec",
            "range": "stddev: 0.00009711833386984482",
            "extra": "mean: 673.0093278689743 usec\nrounds: 610"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_count",
            "value": 910.0101942088629,
            "unit": "iter/sec",
            "range": "stddev: 0.00017649865728141783",
            "extra": "mean: 1.0988887886793088 msec\nrounds: 530"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_count",
            "value": 1072.6635745386247,
            "unit": "iter/sec",
            "range": "stddev: 0.00008100038263552563",
            "extra": "mean: 932.2587470448235 usec\nrounds: 423"
          },
          {
            "name": "benchmarks/bench_schema.py::test_cqlengine_sync_table_create",
            "value": 7275.888687371101,
            "unit": "iter/sec",
            "range": "stddev: 0.00005868032513020622",
            "extra": "mean: 137.44025547500735 usec\nrounds: 137"
          },
          {
            "name": "benchmarks/bench_schema.py::test_coodie_sync_table_create",
            "value": 55353.77449017587,
            "unit": "iter/sec",
            "range": "stddev: 0.00000531063359378073",
            "extra": "mean: 18.065615384141125 usec\nrounds: 169"
          },
          {
            "name": "benchmarks/bench_schema.py::test_cqlengine_sync_table_noop",
            "value": 5743.876397569397,
            "unit": "iter/sec",
            "range": "stddev: 0.00006131009257346094",
            "extra": "mean: 174.0984538635205 usec\nrounds: 2666"
          },
          {
            "name": "benchmarks/bench_schema.py::test_coodie_sync_table_noop",
            "value": 56624.369901083024,
            "unit": "iter/sec",
            "range": "stddev: 0.000010628644454741607",
            "extra": "mean: 17.660240665757474 usec\nrounds: 6669"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_cqlengine_model_instantiation",
            "value": 75946.85130037805,
            "unit": "iter/sec",
            "range": "stddev: 0.000017468602710820193",
            "extra": "mean: 13.167102820956872 usec\nrounds: 19461"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 474193.39099469985,
            "unit": "iter/sec",
            "range": "stddev: 4.814417270453993e-7",
            "extra": "mean: 2.1088442373739813 usec\nrounds: 31548"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_cqlengine_model_serialization",
            "value": 201536.02935140554,
            "unit": "iter/sec",
            "range": "stddev: 8.905846195508317e-7",
            "extra": "mean: 4.961891941695268 usec\nrounds: 37452"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 505375.4273822795,
            "unit": "iter/sec",
            "range": "stddev: 4.74402421174245e-7",
            "extra": "mean: 1.978726993474444 usec\nrounds: 31578"
          },
          {
            "name": "benchmarks/bench_update.py::test_cqlengine_partial_update",
            "value": 1944.8983920428684,
            "unit": "iter/sec",
            "range": "stddev: 0.00007148231195333413",
            "extra": "mean: 514.1656778016188 usec\nrounds: 928"
          },
          {
            "name": "benchmarks/bench_update.py::test_coodie_partial_update",
            "value": 1039.7704220962246,
            "unit": "iter/sec",
            "range": "stddev: 0.000027165241626470688",
            "extra": "mean: 961.7507660815687 usec\nrounds: 513"
          },
          {
            "name": "benchmarks/bench_update.py::test_cqlengine_update_if_condition",
            "value": 817.3586045866228,
            "unit": "iter/sec",
            "range": "stddev: 0.00011931178873504673",
            "extra": "mean: 1.223453199597437 msec\nrounds: 496"
          },
          {
            "name": "benchmarks/bench_update.py::test_coodie_update_if_condition",
            "value": 662.9838142751913,
            "unit": "iter/sec",
            "range": "stddev: 0.00012786835621982095",
            "extra": "mean: 1.508332448648467 msec\nrounds: 370"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "c927dc8334fb08358e7b40dc65e53b61f8f70885",
          "message": "docs: improve landing page by embedding README sections via include markers\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-02-26T16:39:26+02:00",
          "tree_id": "83bf98c3767e1a061f0a6e9697adbae48aff4818",
          "url": "https://github.com/fruch/coodie/commit/c927dc8334fb08358e7b40dc65e53b61f8f70885"
        },
        "date": 1772116841094,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_get_or_create_user",
            "value": 1327.6735499888011,
            "unit": "iter/sec",
            "range": "stddev: 0.00019559926749327362",
            "extra": "mean: 753.1971997246122 usec\nrounds: 726"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_get_or_create_user",
            "value": 2067.141045910057,
            "unit": "iter/sec",
            "range": "stddev: 0.000020477401636923105",
            "extra": "mean: 483.7599262897665 usec\nrounds: 814"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_filter_runs_by_status",
            "value": 872.8357558139392,
            "unit": "iter/sec",
            "range": "stddev: 0.0007311381909361103",
            "extra": "mean: 1.1456909198999041 msec\nrounds: 799"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_filter_runs_by_status",
            "value": 2057.68835534531,
            "unit": "iter/sec",
            "range": "stddev: 0.000032542965259657185",
            "extra": "mean: 485.98224186975364 usec\nrounds: 984"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_latest_runs",
            "value": 1007.7503646476986,
            "unit": "iter/sec",
            "range": "stddev: 0.00008049833393485911",
            "extra": "mean: 992.3092415348241 usec\nrounds: 886"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_latest_runs",
            "value": 2076.8473250561356,
            "unit": "iter/sec",
            "range": "stddev: 0.000023988588356422895",
            "extra": "mean: 481.49904325440525 usec\nrounds: 971"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_list_mutation",
            "value": 1303.1064563862346,
            "unit": "iter/sec",
            "range": "stddev: 0.00007456222397469905",
            "extra": "mean: 767.3970112719667 usec\nrounds: 621"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_list_mutation",
            "value": 1018.2355979307576,
            "unit": "iter/sec",
            "range": "stddev: 0.000023631712681538107",
            "extra": "mean: 982.0909836900067 usec\nrounds: 981"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_batch_events",
            "value": 332.5166879954294,
            "unit": "iter/sec",
            "range": "stddev: 0.00012345220402794997",
            "extra": "mean: 3.007367858823812 msec\nrounds: 255"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_batch_events",
            "value": 857.2137557657827,
            "unit": "iter/sec",
            "range": "stddev: 0.00005678607373177858",
            "extra": "mean: 1.166570173744658 msec\nrounds: 518"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_notification_feed",
            "value": 729.2256885276511,
            "unit": "iter/sec",
            "range": "stddev: 0.00011571258669555659",
            "extra": "mean: 1.3713175711336472 msec\nrounds: 485"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_notification_feed",
            "value": 1464.032300491418,
            "unit": "iter/sec",
            "range": "stddev: 0.000057940248500652155",
            "extra": "mean: 683.0450391458845 usec\nrounds: 843"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_status_update",
            "value": 1145.3474152208096,
            "unit": "iter/sec",
            "range": "stddev: 0.00007268510004597758",
            "extra": "mean: 873.0975306799917 usec\nrounds: 603"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_status_update",
            "value": 1030.4622458667122,
            "unit": "iter/sec",
            "range": "stddev: 0.00002536454209077458",
            "extra": "mean: 970.4382707965291 usec\nrounds: 565"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_comment_with_collections",
            "value": 1280.0816625130244,
            "unit": "iter/sec",
            "range": "stddev: 0.00006336975539041024",
            "extra": "mean: 781.2001603372905 usec\nrounds: 711"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_comment_with_collections",
            "value": 2036.4271529561024,
            "unit": "iter/sec",
            "range": "stddev: 0.000022024232961317075",
            "extra": "mean: 491.0561119499845 usec\nrounds: 795"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_multi_model_lookup",
            "value": 723.036681375738,
            "unit": "iter/sec",
            "range": "stddev: 0.00010696512658734226",
            "extra": "mean: 1.383055695178947 msec\nrounds: 643"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_multi_model_lookup",
            "value": 1029.7892527094584,
            "unit": "iter/sec",
            "range": "stddev: 0.00002394959810827335",
            "extra": "mean: 971.0724765954972 usec\nrounds: 705"
          },
          {
            "name": "benchmarks/bench_argus.py::test_cqlengine_argus_model_instantiation",
            "value": 27349.02726227067,
            "unit": "iter/sec",
            "range": "stddev: 0.000024469618860396924",
            "extra": "mean: 36.56437175663463 usec\nrounds: 11408"
          },
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 46862.09197144267,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021032109245813855",
            "extra": "mean: 21.33920953869048 usec\nrounds: 18011"
          },
          {
            "name": "benchmarks/bench_batch.py::test_cqlengine_batch_insert_10",
            "value": 585.9488554257478,
            "unit": "iter/sec",
            "range": "stddev: 0.00009518270989665517",
            "extra": "mean: 1.7066335922329 msec\nrounds: 412"
          },
          {
            "name": "benchmarks/bench_batch.py::test_coodie_batch_insert_10",
            "value": 1714.5221630574445,
            "unit": "iter/sec",
            "range": "stddev: 0.00017670094812276775",
            "extra": "mean: 583.2528861666838 usec\nrounds: 694"
          },
          {
            "name": "benchmarks/bench_batch.py::test_cqlengine_batch_insert_100",
            "value": 18.875478074755446,
            "unit": "iter/sec",
            "range": "stddev: 0.0004192433258731758",
            "extra": "mean: 52.978790578948356 msec\nrounds: 19"
          },
          {
            "name": "benchmarks/bench_batch.py::test_coodie_batch_insert_100",
            "value": 487.01140963256404,
            "unit": "iter/sec",
            "range": "stddev: 0.0003048487548325606",
            "extra": "mean: 2.0533399838711603 msec\nrounds: 248"
          },
          {
            "name": "benchmarks/bench_collections.py::test_cqlengine_collection_write",
            "value": 1394.3099571354744,
            "unit": "iter/sec",
            "range": "stddev: 0.0002166997692424508",
            "extra": "mean: 717.2006445786558 usec\nrounds: 664"
          },
          {
            "name": "benchmarks/bench_collections.py::test_coodie_collection_write",
            "value": 2034.5759994472521,
            "unit": "iter/sec",
            "range": "stddev: 0.0000171628885346366",
            "extra": "mean: 491.5028980346162 usec\nrounds: 814"
          },
          {
            "name": "benchmarks/bench_collections.py::test_cqlengine_collection_read",
            "value": 1441.3511356286072,
            "unit": "iter/sec",
            "range": "stddev: 0.00006984124056867183",
            "extra": "mean: 693.7934659231227 usec\nrounds: 807"
          },
          {
            "name": "benchmarks/bench_collections.py::test_coodie_collection_read",
            "value": 2091.7163847739107,
            "unit": "iter/sec",
            "range": "stddev: 0.00001577512916192129",
            "extra": "mean: 478.0762857140826 usec\nrounds: 770"
          },
          {
            "name": "benchmarks/bench_collections.py::test_cqlengine_collection_roundtrip",
            "value": 715.4629630505837,
            "unit": "iter/sec",
            "range": "stddev: 0.00010108144723807525",
            "extra": "mean: 1.397696389113156 msec\nrounds: 496"
          },
          {
            "name": "benchmarks/bench_collections.py::test_coodie_collection_roundtrip",
            "value": 1032.5457466016542,
            "unit": "iter/sec",
            "range": "stddev: 0.00002520120429748372",
            "extra": "mean: 968.4800923263983 usec\nrounds: 834"
          },
          {
            "name": "benchmarks/bench_delete.py::test_cqlengine_single_delete",
            "value": 898.2085826604506,
            "unit": "iter/sec",
            "range": "stddev: 0.00007781139284381621",
            "extra": "mean: 1.113327148398035 msec\nrounds: 593"
          },
          {
            "name": "benchmarks/bench_delete.py::test_coodie_single_delete",
            "value": 1032.0665830388027,
            "unit": "iter/sec",
            "range": "stddev: 0.000025090295850421447",
            "extra": "mean: 968.9297342189044 usec\nrounds: 602"
          },
          {
            "name": "benchmarks/bench_delete.py::test_cqlengine_bulk_delete",
            "value": 836.1304886023211,
            "unit": "iter/sec",
            "range": "stddev: 0.00009157345234882912",
            "extra": "mean: 1.1959855711894969 msec\nrounds: 597"
          },
          {
            "name": "benchmarks/bench_delete.py::test_coodie_bulk_delete",
            "value": 1041.5788198707983,
            "unit": "iter/sec",
            "range": "stddev: 0.000023850952496636143",
            "extra": "mean: 960.0809664352087 usec\nrounds: 864"
          },
          {
            "name": "benchmarks/bench_insert.py::test_cqlengine_single_insert",
            "value": 1610.145905275068,
            "unit": "iter/sec",
            "range": "stddev: 0.00006244525313889816",
            "extra": "mean: 621.0617290792451 usec\nrounds: 956"
          },
          {
            "name": "benchmarks/bench_insert.py::test_coodie_single_insert",
            "value": 2091.579159452642,
            "unit": "iter/sec",
            "range": "stddev: 0.000016696720720729134",
            "extra": "mean: 478.1076515706419 usec\nrounds: 1369"
          },
          {
            "name": "benchmarks/bench_insert.py::test_cqlengine_insert_if_not_exists",
            "value": 717.9932856214404,
            "unit": "iter/sec",
            "range": "stddev: 0.0003415476383686109",
            "extra": "mean: 1.392770684665214 msec\nrounds: 463"
          },
          {
            "name": "benchmarks/bench_insert.py::test_coodie_insert_if_not_exists",
            "value": 835.2266459363657,
            "unit": "iter/sec",
            "range": "stddev: 0.00033220937964893553",
            "extra": "mean: 1.1972798100555189 msec\nrounds: 537"
          },
          {
            "name": "benchmarks/bench_insert.py::test_cqlengine_insert_with_ttl",
            "value": 1557.8533926828495,
            "unit": "iter/sec",
            "range": "stddev: 0.00014125339147084693",
            "extra": "mean: 641.908927179505 usec\nrounds: 975"
          },
          {
            "name": "benchmarks/bench_insert.py::test_coodie_insert_with_ttl",
            "value": 2030.7578297546218,
            "unit": "iter/sec",
            "range": "stddev: 0.000018683704375010583",
            "extra": "mean: 492.42700697642067 usec\nrounds: 860"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_get_by_pk",
            "value": 1493.6666115621722,
            "unit": "iter/sec",
            "range": "stddev: 0.00006410306177826187",
            "extra": "mean: 669.4934413470861 usec\nrounds: 861"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_get_by_pk",
            "value": 2071.3714328248493,
            "unit": "iter/sec",
            "range": "stddev: 0.0000180863683816498",
            "extra": "mean: 482.7719375448961 usec\nrounds: 1393"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_filter_secondary_index",
            "value": 194.71195858622548,
            "unit": "iter/sec",
            "range": "stddev: 0.0019470861538128652",
            "extra": "mean: 5.135791387754769 msec\nrounds: 196"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_filter_secondary_index",
            "value": 543.0619188040266,
            "unit": "iter/sec",
            "range": "stddev: 0.00007147680003287628",
            "extra": "mean: 1.8414106483516244 msec\nrounds: 364"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_filter_limit",
            "value": 759.4548257072221,
            "unit": "iter/sec",
            "range": "stddev: 0.00017982611025194815",
            "extra": "mean: 1.3167340125448235 msec\nrounds: 558"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_filter_limit",
            "value": 1545.8303325605425,
            "unit": "iter/sec",
            "range": "stddev: 0.00010920846099713462",
            "extra": "mean: 646.9015253074903 usec\nrounds: 731"
          },
          {
            "name": "benchmarks/bench_read.py::test_cqlengine_count",
            "value": 949.3548184658267,
            "unit": "iter/sec",
            "range": "stddev: 0.00006699202209921113",
            "extra": "mean: 1.0533469473679153 msec\nrounds: 570"
          },
          {
            "name": "benchmarks/bench_read.py::test_coodie_count",
            "value": 1055.3458556795933,
            "unit": "iter/sec",
            "range": "stddev: 0.00004643006474300292",
            "extra": "mean: 947.5566655407451 usec\nrounds: 592"
          },
          {
            "name": "benchmarks/bench_schema.py::test_cqlengine_sync_table_create",
            "value": 5613.248897324321,
            "unit": "iter/sec",
            "range": "stddev: 0.00005819740526406795",
            "extra": "mean: 178.14994814797402 usec\nrounds: 135"
          },
          {
            "name": "benchmarks/bench_schema.py::test_coodie_sync_table_create",
            "value": 45120.65496560607,
            "unit": "iter/sec",
            "range": "stddev: 0.00000567398186913328",
            "extra": "mean: 22.16279885037719 usec\nrounds: 174"
          },
          {
            "name": "benchmarks/bench_schema.py::test_cqlengine_sync_table_noop",
            "value": 4530.521010059001,
            "unit": "iter/sec",
            "range": "stddev: 0.00005952612680536822",
            "extra": "mean: 220.72516555595377 usec\nrounds: 2851"
          },
          {
            "name": "benchmarks/bench_schema.py::test_coodie_sync_table_noop",
            "value": 44714.645843391154,
            "unit": "iter/sec",
            "range": "stddev: 0.00001178437151025893",
            "extra": "mean: 22.364037132316916 usec\nrounds: 7002"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_cqlengine_model_instantiation",
            "value": 83477.11932347814,
            "unit": "iter/sec",
            "range": "stddev: 0.000017932336193721432",
            "extra": "mean: 11.979330481265754 usec\nrounds: 22440"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 502063.32769881224,
            "unit": "iter/sec",
            "range": "stddev: 4.2951129816010864e-7",
            "extra": "mean: 1.9917806078039222 usec\nrounds: 37809"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_cqlengine_model_serialization",
            "value": 225229.60011902204,
            "unit": "iter/sec",
            "range": "stddev: 6.995231447445255e-7",
            "extra": "mean: 4.439913756768881 usec\nrounds: 43644"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 507140.8731559777,
            "unit": "iter/sec",
            "range": "stddev: 4.3553788792699297e-7",
            "extra": "mean: 1.9718386999196518 usec\nrounds: 36336"
          },
          {
            "name": "benchmarks/bench_update.py::test_cqlengine_partial_update",
            "value": 1839.6027445464906,
            "unit": "iter/sec",
            "range": "stddev: 0.00006182010125464703",
            "extra": "mean: 543.5956230031205 usec\nrounds: 939"
          },
          {
            "name": "benchmarks/bench_update.py::test_coodie_partial_update",
            "value": 1046.7253457328748,
            "unit": "iter/sec",
            "range": "stddev: 0.000012932026928274014",
            "extra": "mean: 955.3604525548585 usec\nrounds: 548"
          },
          {
            "name": "benchmarks/bench_update.py::test_cqlengine_update_if_condition",
            "value": 762.2703980361472,
            "unit": "iter/sec",
            "range": "stddev: 0.0003247251390305574",
            "extra": "mean: 1.31187043675882 msec\nrounds: 506"
          },
          {
            "name": "benchmarks/bench_update.py::test_coodie_update_if_condition",
            "value": 592.7793478794295,
            "unit": "iter/sec",
            "range": "stddev: 0.000432367323990398",
            "extra": "mean: 1.6869683526886274 msec\nrounds: 465"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "d56cc561a3ac772f4dc31a2e1364e379789f4103",
          "message": "feat(usertype): add full UDT support with frozen UDTs, nested types, and driver integration\n\nEnables modeling Cassandra user-defined types (UDTs) as Pydantic models via the UserType base class,\nbringing coodie's type-safe ORM to complex composite data structures.\nFrozen semantics match cqlengine's behavior while leveraging Pydantic's validation.\nIncludes CQL DDL generation with dependency ordering, serialization round-trips,\nbenchmarks comparing performance against cqlengine, and comprehensive documentation\ncovering migration patterns and frozen collection semantics.\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-02-27T16:06:20+02:00",
          "tree_id": "dbfee4f230e1cd64b62a7234d9ed5dad3d8abb81",
          "url": "https://github.com/fruch/coodie/commit/d56cc561a3ac772f4dc31a2e1364e379789f4103"
        },
        "date": 1772201213053,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 79975.43210203783,
            "unit": "iter/sec",
            "range": "stddev: 8.827191033216893e-7",
            "extra": "mean: 12.503839913289063 usec\nrounds: 8764"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 529648.5484145145,
            "unit": "iter/sec",
            "range": "stddev: 5.64246717585607e-7",
            "extra": "mean: 1.8880444456866108 usec\nrounds: 35594"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 666619.3343712304,
            "unit": "iter/sec",
            "range": "stddev: 3.024924852996252e-7",
            "extra": "mean: 1.5001065052264366 usec\nrounds: 40552"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 937194.000405971,
            "unit": "iter/sec",
            "range": "stddev: 2.374159916393722e-7",
            "extra": "mean: 1.067014939880988 usec\nrounds: 111112"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 984367.4146917526,
            "unit": "iter/sec",
            "range": "stddev: 2.1983695338126337e-7",
            "extra": "mean: 1.0158808439561589 usec\nrounds: 87398"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 829416.1876878095,
            "unit": "iter/sec",
            "range": "stddev: 2.4419085786397753e-7",
            "extra": "mean: 1.2056673294353375 usec\nrounds: 88520"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 189556.84605644984,
            "unit": "iter/sec",
            "range": "stddev: 5.566941490636374e-7",
            "extra": "mean: 5.275462325967383 usec\nrounds: 7326"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "8501cdd890e955c82b5c4c32b76d8a5848bd4b53",
          "message": "feat(ci): extract resolve-conflicts script, add Bats tests, document act commands\n\n- Extract conflict-resolution loop into .github/scripts/resolve-conflicts.sh\n  (Phase 2 of github-actions-testing-plan.md: shell scripts in .github/scripts/)\n- Update pr-rebase-squash.yml to call bash .github/scripts/resolve-conflicts.sh\n  (npm install stays in the workflow; resolution logic lives in the script)\n- Add 9 Bats tests in tests/workflows/test_resolve_conflicts.bats:\n  no conflicts, Copilot resolves, empty response, markers still present,\n  fenced-block stripping, multi-round rebase, MAX_ROUNDS exceeded\n- Add testing docs to CONTRIBUTING.md:\n  bats/pytest commands, workflow_dispatch gh-workflow-run (preferred),\n  and act command with event payload template\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-02-28T21:49:16+02:00",
          "tree_id": "31aad9dd9842af1b1684028fafbc5b15f282cd88",
          "url": "https://github.com/fruch/coodie/commit/8501cdd890e955c82b5c4c32b76d8a5848bd4b53"
        },
        "date": 1772308196726,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 52952.85080363864,
            "unit": "iter/sec",
            "range": "stddev: 0.000001903274642150638",
            "extra": "mean: 18.88472452046501 usec\nrounds: 8919"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 552497.605151093,
            "unit": "iter/sec",
            "range": "stddev: 4.0314716926527934e-7",
            "extra": "mean: 1.809962596537459 usec\nrounds: 50824"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 586122.8590104614,
            "unit": "iter/sec",
            "range": "stddev: 5.222644560408868e-7",
            "extra": "mean: 1.7061269401576975 usec\nrounds: 57531"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 814728.4960397246,
            "unit": "iter/sec",
            "range": "stddev: 3.430682721484332e-7",
            "extra": "mean: 1.227402754243718 usec\nrounds: 158958"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 927346.0470888306,
            "unit": "iter/sec",
            "range": "stddev: 3.3987188694459854e-7",
            "extra": "mean: 1.0783461073018517 usec\nrounds: 95612"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 732444.8690393802,
            "unit": "iter/sec",
            "range": "stddev: 3.988477732317359e-7",
            "extra": "mean: 1.3652904706828313 usec\nrounds: 127796"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 184076.0816737709,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010932552939594178",
            "extra": "mean: 5.432536323606949 usec\nrounds: 6800"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "e84ff7e9f023b723105006c470d9d209d767175c",
          "message": "docs(perf): add Phase 6 dict_factory analysis to performance plan (§13C)\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-02-28T21:53:24+02:00",
          "tree_id": "95b5afcbb57477d74295120b716b4dc57b779c35",
          "url": "https://github.com/fruch/coodie/commit/e84ff7e9f023b723105006c470d9d209d767175c"
        },
        "date": 1772308442843,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 52665.533008989485,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018215912539998978",
            "extra": "mean: 18.987750486248945 usec\nrounds: 8224"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 580461.1344999097,
            "unit": "iter/sec",
            "range": "stddev: 4.1529710839428993e-7",
            "extra": "mean: 1.7227682278186287 usec\nrounds: 42490"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 623579.6414169982,
            "unit": "iter/sec",
            "range": "stddev: 4.142689001378457e-7",
            "extra": "mean: 1.6036444001405157 usec\nrounds: 47126"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 842829.6866396889,
            "unit": "iter/sec",
            "range": "stddev: 3.4576879313150125e-7",
            "extra": "mean: 1.1864793277357606 usec\nrounds: 153563"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 932409.7452662613,
            "unit": "iter/sec",
            "range": "stddev: 3.1061414595952236e-7",
            "extra": "mean: 1.0724898630423876 usec\nrounds: 91744"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 736671.0751821117,
            "unit": "iter/sec",
            "range": "stddev: 3.644106513223114e-7",
            "extra": "mean: 1.3574579397634028 usec\nrounds: 102365"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 189489.4926117755,
            "unit": "iter/sec",
            "range": "stddev: 6.980307183958852e-7",
            "extra": "mean: 5.277337472472903 usec\nrounds: 7731"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "9f03612c1782c7b7ca2a6cd03fe64edbbbbabbe8",
          "message": "feat(drivers): add explicit SSL parameters to init_coodie/init_coodie_async (Phase 2+3)\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-02-28T22:04:07+02:00",
          "tree_id": "c0a34334639a4d855fd3769cb3ec864db88c1c38",
          "url": "https://github.com/fruch/coodie/commit/9f03612c1782c7b7ca2a6cd03fe64edbbbbabbe8"
        },
        "date": 1772309086220,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 53374.06261791804,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015641529795804126",
            "extra": "mean: 18.735692037508365 usec\nrounds: 12810"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 576941.4090326291,
            "unit": "iter/sec",
            "range": "stddev: 4.6317244771623345e-7",
            "extra": "mean: 1.733278257278712 usec\nrounds: 55729"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 604839.6289506222,
            "unit": "iter/sec",
            "range": "stddev: 3.96179171936383e-7",
            "extra": "mean: 1.6533308204936383 usec\nrounds: 60489"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 824621.0187891856,
            "unit": "iter/sec",
            "range": "stddev: 3.433096794360781e-7",
            "extra": "mean: 1.212678281555724 usec\nrounds: 155232"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 953415.4242127949,
            "unit": "iter/sec",
            "range": "stddev: 3.0341887392703737e-7",
            "extra": "mean: 1.048860732272785 usec\nrounds: 129786"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 702281.9135939034,
            "unit": "iter/sec",
            "range": "stddev: 3.4713495087323556e-7",
            "extra": "mean: 1.4239295938614376 usec\nrounds: 131338"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 191200.72140517368,
            "unit": "iter/sec",
            "range": "stddev: 9.185922032501682e-7",
            "extra": "mean: 5.230105789616237 usec\nrounds: 7997"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "340979+fruch@users.noreply.github.com",
            "name": "fruch",
            "username": "fruch"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "46f681e8059c325df8ce7a1d2c26e0a9ae2a9f20",
          "message": "feat(ci): use Copilot to summarize CI failures before commenting on PR\n\n  2c16588 --stat && git --no-pager show 46cc2a7 --stat\n\nAdd a Copilot-powered failure summarization step to the self-healing CI workflow. When a PR build fails, the workflow now calls the GitHub Copilot API to generate a human-readable summary of the failure before posting the comment, making it easier to diagnose issues at a glance.\n\nThe summarization logic is extracted into `.github/scripts/summarize-failure.py` so it can be unit-tested in isolation. Tests live in `tests/workflows/test_summarize_failure.py` and cover both successful summarization and fallback behaviour when the API is unavailable.",
          "timestamp": "2026-02-28T22:06:01+02:00",
          "tree_id": "a2a8ae87e3a4fb43b865b0a8391385a71083af53",
          "url": "https://github.com/fruch/coodie/commit/46f681e8059c325df8ce7a1d2c26e0a9ae2a9f20"
        },
        "date": 1772309195050,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 52845.79882470708,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018772676323635863",
            "extra": "mean: 18.922980108921514 usec\nrounds: 8446"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 573204.0429413859,
            "unit": "iter/sec",
            "range": "stddev: 5.095924737924179e-7",
            "extra": "mean: 1.7445794605155236 usec\nrounds: 44821"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 594085.4311413614,
            "unit": "iter/sec",
            "range": "stddev: 3.940784690893697e-7",
            "extra": "mean: 1.6832595912658428 usec\nrounds: 53434"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 833191.6938912056,
            "unit": "iter/sec",
            "range": "stddev: 3.235303024946946e-7",
            "extra": "mean: 1.2002039954692294 usec\nrounds: 158680"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 953452.4503687714,
            "unit": "iter/sec",
            "range": "stddev: 3.31369121344661e-7",
            "extra": "mean: 1.0488200010532513 usec\nrounds: 95795"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 709703.0481143991,
            "unit": "iter/sec",
            "range": "stddev: 3.7395685640031854e-7",
            "extra": "mean: 1.4090400240732899 usec\nrounds: 96442"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 192761.2602266143,
            "unit": "iter/sec",
            "range": "stddev: 6.489976138514164e-7",
            "extra": "mean: 5.187764381828477 usec\nrounds: 7805"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "1785810bf316ca4d271d4fe33e86c82a0f513716",
          "message": "fix(ci): remove ruff/linting from demo workflow, rely on repo-level pre-commit\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-02-28T22:24:48+02:00",
          "tree_id": "19c1eb78a68d3fc4f773bfe3512047b03363f46a",
          "url": "https://github.com/fruch/coodie/commit/1785810bf316ca4d271d4fe33e86c82a0f513716"
        },
        "date": 1772310328345,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 51858.6718361742,
            "unit": "iter/sec",
            "range": "stddev: 0.000001576161042394402",
            "extra": "mean: 19.283178002689347 usec\nrounds: 8101"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 574513.0209201435,
            "unit": "iter/sec",
            "range": "stddev: 4.511702863197201e-7",
            "extra": "mean: 1.7406045878618976 usec\nrounds: 41109"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 599383.290896031,
            "unit": "iter/sec",
            "range": "stddev: 3.7881859116183604e-7",
            "extra": "mean: 1.6683815101102977 usec\nrounds: 47215"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 828428.053449127,
            "unit": "iter/sec",
            "range": "stddev: 3.3925229696610385e-7",
            "extra": "mean: 1.2071054279687174 usec\nrounds: 147864"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 950810.788037146,
            "unit": "iter/sec",
            "range": "stddev: 4.5017515693747185e-7",
            "extra": "mean: 1.0517339649294475 usec\nrounds: 92251"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 721624.6060000886,
            "unit": "iter/sec",
            "range": "stddev: 3.793712014666381e-7",
            "extra": "mean: 1.3857620592276163 usec\nrounds: 88480"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 188953.72748633043,
            "unit": "iter/sec",
            "range": "stddev: 7.280644300934445e-7",
            "extra": "mean: 5.2923009950800965 usec\nrounds: 7638"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "340979+fruch@users.noreply.github.com",
            "name": "fruch",
            "username": "fruch"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "fe2320cc007d5c307ea4f412e6042799294263a7",
          "message": "feat(ci): implement plan-phase-continuation GitHub Actions workflow\n\n✗ View commit subjects\n  ac5a788 c67bdee 2>/dev/null | head -10\n  Permission denied and could not request permission from user\n\nImplement a GitHub Actions workflow that automatically detects the next incomplete phase in a plan file after a PR is merged and opens a new PR to continue it.\n\nAdd `parse-plan.py` to parse `docs/plans/*.md` files and extract phase status, along with a comprehensive test suite (`test_parse_plan.py`). The workflow (`plan-continuation.yml`) triggers on PR merge to master (when the PR body references a plan file and phase) or via `workflow_dispatch`, resolves merge conflicts with retries, and opens a follow-up PR targeting the next pending phase.\n\nAdd `.github/PULL_REQUEST_TEMPLATE.md` to standardise PR bodies with `Plan:` and `Phase:` fields. Document the workflow in `CONTRIBUTING.md` and add a `writing-plans` skill covering plan file conventions. Fix several shellcheck violations (SC2070, SC2086, SC2129) and a ruff-format issue surfaced during CI runs.",
          "timestamp": "2026-02-28T22:26:31+02:00",
          "tree_id": "6a68ad3ba09d5a60199f38f96f464a645d63bca0",
          "url": "https://github.com/fruch/coodie/commit/fe2320cc007d5c307ea4f412e6042799294263a7"
        },
        "date": 1772310429029,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 52736.53733766329,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016266780211030138",
            "extra": "mean: 18.96218543127255 usec\nrounds: 8580"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 573191.0255753782,
            "unit": "iter/sec",
            "range": "stddev: 4.370491758215008e-7",
            "extra": "mean: 1.7446190805171526 usec\nrounds: 43437"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 612994.14572181,
            "unit": "iter/sec",
            "range": "stddev: 3.589126487278891e-7",
            "extra": "mean: 1.6313369499189663 usec\nrounds: 42858"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 835000.3098325076,
            "unit": "iter/sec",
            "range": "stddev: 3.590678342265933e-7",
            "extra": "mean: 1.1976043460398111 usec\nrounds: 146800"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 937156.585193087,
            "unit": "iter/sec",
            "range": "stddev: 4.0790581067861707e-7",
            "extra": "mean: 1.0670575395828488 usec\nrounds: 90164"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 748797.6073834979,
            "unit": "iter/sec",
            "range": "stddev: 3.3765577771945046e-7",
            "extra": "mean: 1.3354743526682349 usec\nrounds: 97476"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 184727.7737442232,
            "unit": "iter/sec",
            "range": "stddev: 7.002099945654007e-7",
            "extra": "mean: 5.413371144636944 usec\nrounds: 7749"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "75a9fb15aa67b4dd5cfea93c2702212febe82621",
          "message": "docs(plans): add plan for PR conflict detection and /solve command workflows\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-02-28T22:56:00+02:00",
          "tree_id": "b27036a8ae54aee292d07dbbc7e12ad2d37e69f1",
          "url": "https://github.com/fruch/coodie/commit/75a9fb15aa67b4dd5cfea93c2702212febe82621"
        },
        "date": 1772312197807,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 79080.15831840862,
            "unit": "iter/sec",
            "range": "stddev: 9.898490297025557e-7",
            "extra": "mean: 12.645397040982097 usec\nrounds: 8717"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 566372.7810977976,
            "unit": "iter/sec",
            "range": "stddev: 3.4711486178662017e-7",
            "extra": "mean: 1.7656215718236055 usec\nrounds: 36752"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 689492.5725869529,
            "unit": "iter/sec",
            "range": "stddev: 2.954369803150606e-7",
            "extra": "mean: 1.4503419467566323 usec\nrounds: 45393"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 923753.6774141251,
            "unit": "iter/sec",
            "range": "stddev: 3.0172430965059155e-7",
            "extra": "mean: 1.0825396687992757 usec\nrounds: 104844"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 895523.8200983224,
            "unit": "iter/sec",
            "range": "stddev: 4.24915101921338e-7",
            "extra": "mean: 1.1166648809969195 usec\nrounds: 83809"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 828203.4836419988,
            "unit": "iter/sec",
            "range": "stddev: 2.642405727767717e-7",
            "extra": "mean: 1.2074327381509329 usec\nrounds: 82796"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 192822.52684163206,
            "unit": "iter/sec",
            "range": "stddev: 6.303075188030962e-7",
            "extra": "mean: 5.186116043491715 usec\nrounds: 7592"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "95af4604754c6dad3bb79cad28d3a8048efa37fe",
          "message": "fix(ci): add workflows write permission to pr-rebase-squash for force-pushing branches with workflow changes\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-02-28T22:57:20+02:00",
          "tree_id": "9e8732608879b7b2f4b78f22733501e091333b9b",
          "url": "https://github.com/fruch/coodie/commit/95af4604754c6dad3bb79cad28d3a8048efa37fe"
        },
        "date": 1772312276617,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 52876.848376284346,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015516924738722663",
            "extra": "mean: 18.911868439733016 usec\nrounds: 8460"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 550997.0182920061,
            "unit": "iter/sec",
            "range": "stddev: 7.268230019919866e-7",
            "extra": "mean: 1.8148918538612502 usec\nrounds: 39798"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 620912.6736281362,
            "unit": "iter/sec",
            "range": "stddev: 4.2172078339773314e-7",
            "extra": "mean: 1.6105324347090053 usec\nrounds: 47850"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 841297.3640996347,
            "unit": "iter/sec",
            "range": "stddev: 3.5341730059704266e-7",
            "extra": "mean: 1.1886403579431282 usec\nrounds: 157679"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 954700.0354902198,
            "unit": "iter/sec",
            "range": "stddev: 3.312820027434174e-7",
            "extra": "mean: 1.0474494216254213 usec\nrounds: 96909"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 736301.8282681435,
            "unit": "iter/sec",
            "range": "stddev: 3.89575136307366e-7",
            "extra": "mean: 1.358138689336276 usec\nrounds: 104406"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 188823.82235341507,
            "unit": "iter/sec",
            "range": "stddev: 8.692448410069282e-7",
            "extra": "mean: 5.295941939615725 usec\nrounds: 7785"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "dc534151222a30deff522a3e7435cf6fd90d2843",
          "message": "fix(ci): replace invalid workflows permission with PAT checkout for workflow file pushes\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-01T00:17:33+02:00",
          "tree_id": "cfceafe40cc2cb3d97c150f6d3ca6724157f6e02",
          "url": "https://github.com/fruch/coodie/commit/dc534151222a30deff522a3e7435cf6fd90d2843"
        },
        "date": 1772317088799,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 53850.64346877629,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015859902821539754",
            "extra": "mean: 18.569880238846554 usec\nrounds: 8542"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 574879.978275533,
            "unit": "iter/sec",
            "range": "stddev: 4.6001301189208967e-7",
            "extra": "mean: 1.7394935252393018 usec\nrounds: 49809"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 622189.6218503702,
            "unit": "iter/sec",
            "range": "stddev: 3.8345240208690123e-7",
            "extra": "mean: 1.6072270653213965 usec\nrounds: 55451"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 826024.3654628841,
            "unit": "iter/sec",
            "range": "stddev: 5.065012851822409e-7",
            "extra": "mean: 1.2106180420472514 usec\nrounds: 159439"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 975740.8923632798,
            "unit": "iter/sec",
            "range": "stddev: 3.0616123598367314e-7",
            "extra": "mean: 1.0248622434773271 usec\nrounds: 101948"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 741971.6556353382,
            "unit": "iter/sec",
            "range": "stddev: 3.4200312315856813e-7",
            "extra": "mean: 1.347760379261006 usec\nrounds: 118120"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 190054.4767281102,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010685496928018847",
            "extra": "mean: 5.261649276647078 usec\nrounds: 7533"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "7f50ff0f5cb9d4214f78909cd090660e38c3e352",
          "message": "fix(workflows): use GH_PAT for self-healing comment to work with Copilot PRs\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-01T00:23:05+02:00",
          "tree_id": "7f28664613b427422617e8c0af612d6d0804f906",
          "url": "https://github.com/fruch/coodie/commit/7f50ff0f5cb9d4214f78909cd090660e38c3e352"
        },
        "date": 1772317421536,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 52490.07533452876,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017139914017342482",
            "extra": "mean: 19.051220514103264 usec\nrounds: 8131"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 535302.6631886241,
            "unit": "iter/sec",
            "range": "stddev: 7.311075917266564e-7",
            "extra": "mean: 1.8681020453799442 usec\nrounds: 39894"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 567106.5676904714,
            "unit": "iter/sec",
            "range": "stddev: 7.125917165551985e-7",
            "extra": "mean: 1.7633370110180124 usec\nrounds: 44049"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 811464.0335321975,
            "unit": "iter/sec",
            "range": "stddev: 3.687981232127139e-7",
            "extra": "mean: 1.2323405088542618 usec\nrounds: 147864"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 943291.4441392714,
            "unit": "iter/sec",
            "range": "stddev: 2.948700538082048e-7",
            "extra": "mean: 1.0601177464431193 usec\nrounds: 83459"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 712613.930658404,
            "unit": "iter/sec",
            "range": "stddev: 3.879748308445154e-7",
            "extra": "mean: 1.4032843829983395 usec\nrounds: 94429"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 190983.61926225614,
            "unit": "iter/sec",
            "range": "stddev: 7.007906657594986e-7",
            "extra": "mean: 5.236051153825991 usec\nrounds: 7800"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "b82906349b26c1cfa087dc42442dc49c2ce6d720",
          "message": "feat(cql_builder): add map__update collection operator and phase 2 unit tests\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-01T00:27:29+02:00",
          "tree_id": "a32b5ab8544e17c28bff03d01d1e90556911c23d",
          "url": "https://github.com/fruch/coodie/commit/b82906349b26c1cfa087dc42442dc49c2ce6d720"
        },
        "date": 1772317708259,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 52545.809989607325,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017356876125362942",
            "extra": "mean: 19.031013133069663 usec\nrounds: 8604"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 564971.8880126893,
            "unit": "iter/sec",
            "range": "stddev: 5.749787008668005e-7",
            "extra": "mean: 1.7699995720451491 usec\nrounds: 49073"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 620227.3927342263,
            "unit": "iter/sec",
            "range": "stddev: 4.371221324864479e-7",
            "extra": "mean: 1.612311890307802 usec\nrounds: 54843"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 850166.1484828235,
            "unit": "iter/sec",
            "range": "stddev: 3.4170396188069215e-7",
            "extra": "mean: 1.1762406698791346 usec\nrounds: 168862"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 921849.271880521,
            "unit": "iter/sec",
            "range": "stddev: 3.413011110625874e-7",
            "extra": "mean: 1.0847760371498216 usec\nrounds: 96900"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 750757.6719164032,
            "unit": "iter/sec",
            "range": "stddev: 3.359680983083263e-7",
            "extra": "mean: 1.3319877204149966 usec\nrounds: 96909"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 188230.4047549374,
            "unit": "iter/sec",
            "range": "stddev: 0.00000100755138704865",
            "extra": "mean: 5.312637994387405 usec\nrounds: 7638"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "21d7c4af6b3b709893541ae615c04f72e703e49e",
          "message": "feat(demo): add django-taskboard demo (The Hivemind Kanban)\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-01T00:46:29+02:00",
          "tree_id": "ee54b78b5c2adc1b980536a5c76be2c9bc7f38f9",
          "url": "https://github.com/fruch/coodie/commit/21d7c4af6b3b709893541ae615c04f72e703e49e"
        },
        "date": 1772318873592,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 52439.5032347578,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016667968435567727",
            "extra": "mean: 19.069593308755504 usec\nrounds: 8429"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 569131.8218652185,
            "unit": "iter/sec",
            "range": "stddev: 4.937274992283309e-7",
            "extra": "mean: 1.7570621806433089 usec\nrounds: 36008"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 593793.5563839179,
            "unit": "iter/sec",
            "range": "stddev: 5.096198504496982e-7",
            "extra": "mean: 1.6840869848601874 usec\nrounds: 44479"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 806838.4332421806,
            "unit": "iter/sec",
            "range": "stddev: 3.4059489465990105e-7",
            "extra": "mean: 1.239405510198149 usec\nrounds: 105731"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 922596.0079137599,
            "unit": "iter/sec",
            "range": "stddev: 4.3918746756774107e-7",
            "extra": "mean: 1.083898034917007 usec\nrounds: 80302"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 701279.504705264,
            "unit": "iter/sec",
            "range": "stddev: 3.5833624276936404e-7",
            "extra": "mean: 1.425964958751052 usec\nrounds: 88724"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 187886.7060054307,
            "unit": "iter/sec",
            "range": "stddev: 6.810317351723921e-7",
            "extra": "mean: 5.322356335158145 usec\nrounds: 7782"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "daa0d40363d42f358d5d85471e73eb1143c9877f",
          "message": "feat(migrations): implement Phase B migration framework core\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-01T00:48:48+02:00",
          "tree_id": "c7eab623030404acbb63c449209517d8b0fd8c42",
          "url": "https://github.com/fruch/coodie/commit/daa0d40363d42f358d5d85471e73eb1143c9877f"
        },
        "date": 1772318974724,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 52614.01747249444,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019047079549010377",
            "extra": "mean: 19.006341808488205 usec\nrounds: 8771"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 565925.4491998213,
            "unit": "iter/sec",
            "range": "stddev: 4.474062289338687e-7",
            "extra": "mean: 1.767017195310671 usec\nrounds: 45536"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 622616.0677808803,
            "unit": "iter/sec",
            "range": "stddev: 4.2977959132653933e-7",
            "extra": "mean: 1.606126233722471 usec\nrounds: 52894"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 843245.7375385066,
            "unit": "iter/sec",
            "range": "stddev: 3.0684428908522634e-7",
            "extra": "mean: 1.1858939280488627 usec\nrounds: 149210"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 921256.1301720146,
            "unit": "iter/sec",
            "range": "stddev: 3.416936996349159e-7",
            "extra": "mean: 1.08547445954393 usec\nrounds: 94967"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 739548.2205266113,
            "unit": "iter/sec",
            "range": "stddev: 3.7457063556901913e-7",
            "extra": "mean: 1.352176872642501 usec\nrounds: 100513"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 191677.04073400144,
            "unit": "iter/sec",
            "range": "stddev: 7.45573602990041e-7",
            "extra": "mean: 5.217108925360255 usec\nrounds: 7932"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "f9825531a87bb553943d4c4d96b224f909ddd0c5",
          "message": "docs(plans): add Phase 7 benchmark analysis for __slots__ on hot-path classes\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-01T00:53:33+02:00",
          "tree_id": "6517d66aca171901492d64ca0a06ef6080f3b7b5",
          "url": "https://github.com/fruch/coodie/commit/f9825531a87bb553943d4c4d96b224f909ddd0c5"
        },
        "date": 1772319251074,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 52889.859797280515,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014921735410752391",
            "extra": "mean: 18.9072159357741 usec\nrounds: 8961"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 552060.8687111172,
            "unit": "iter/sec",
            "range": "stddev: 6.519049630587915e-7",
            "extra": "mean: 1.8113944615105126 usec\nrounds: 51133"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 617765.2420062214,
            "unit": "iter/sec",
            "range": "stddev: 3.8756957216421137e-7",
            "extra": "mean: 1.618737882941509 usec\nrounds: 58100"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 821498.7290521183,
            "unit": "iter/sec",
            "range": "stddev: 4.2420707873119076e-7",
            "extra": "mean: 1.2172873367118224 usec\nrounds: 152859"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 944945.4063489228,
            "unit": "iter/sec",
            "range": "stddev: 3.534876953470407e-7",
            "extra": "mean: 1.0582621951291313 usec\nrounds: 88724"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 695195.0418338021,
            "unit": "iter/sec",
            "range": "stddev: 4.784474880749325e-7",
            "extra": "mean: 1.438445241729826 usec\nrounds: 113161"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 188103.6257687531,
            "unit": "iter/sec",
            "range": "stddev: 7.787983394300334e-7",
            "extra": "mean: 5.316218631688466 usec\nrounds: 7396"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "8912b50ac710bb3d799c599ba644712c20c01526",
          "message": "docs(plans): create sync API support plan for AcsyllaDriver and PythonRsDriver\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-01T00:54:35+02:00",
          "tree_id": "6317b4d589dc8a8c2a67a2c508283eede8f8a99e",
          "url": "https://github.com/fruch/coodie/commit/8912b50ac710bb3d799c599ba644712c20c01526"
        },
        "date": 1772319307044,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 53467.07059408944,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016200815000601078",
            "extra": "mean: 18.703100597969655 usec\nrounds: 7525"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 576911.1859205036,
            "unit": "iter/sec",
            "range": "stddev: 4.4280947422680305e-7",
            "extra": "mean: 1.7333690599263172 usec\nrounds: 43665"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 611502.2961481344,
            "unit": "iter/sec",
            "range": "stddev: 4.625031313764369e-7",
            "extra": "mean: 1.6353168357650014 usec\nrounds: 46532"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 834202.6404698323,
            "unit": "iter/sec",
            "range": "stddev: 3.405464431221183e-7",
            "extra": "mean: 1.198749502203432 usec\nrounds: 147646"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 938663.0320699321,
            "unit": "iter/sec",
            "range": "stddev: 3.409737389697705e-7",
            "extra": "mean: 1.0653450341969983 usec\nrounds: 94608"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 749408.3169451788,
            "unit": "iter/sec",
            "range": "stddev: 3.5377742198123144e-7",
            "extra": "mean: 1.334386044815076 usec\nrounds: 88254"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 192175.45596314504,
            "unit": "iter/sec",
            "range": "stddev: 7.329184152097304e-7",
            "extra": "mean: 5.2035781311832965 usec\nrounds: 7609"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "c42a7c682c5e5a352d2b3cbe9b7f0de9ea1a9bc7",
          "message": "fix(ci): anchor shell redirect pattern to line-start context\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-01T16:40:14+02:00",
          "tree_id": "d21552bc3b67c7c73b9d67d62e278a55522c90ba",
          "url": "https://github.com/fruch/coodie/commit/c42a7c682c5e5a352d2b3cbe9b7f0de9ea1a9bc7"
        },
        "date": 1772376052527,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 53716.0370912156,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016844000082426694",
            "extra": "mean: 18.616414280560058 usec\nrounds: 8627"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 569590.9704492457,
            "unit": "iter/sec",
            "range": "stddev: 5.55152968802373e-7",
            "extra": "mean: 1.7556458088008027 usec\nrounds: 43341"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 630021.5842565838,
            "unit": "iter/sec",
            "range": "stddev: 3.87961977684764e-7",
            "extra": "mean: 1.5872472070619377 usec\nrounds: 47531"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 854192.7655946834,
            "unit": "iter/sec",
            "range": "stddev: 3.532905841084569e-7",
            "extra": "mean: 1.1706959368870404 usec\nrounds: 138639"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 964981.2765624262,
            "unit": "iter/sec",
            "range": "stddev: 3.789698777202025e-7",
            "extra": "mean: 1.0362895366864753 usec\nrounds: 88013"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 743842.423273105,
            "unit": "iter/sec",
            "range": "stddev: 3.4685550710960943e-7",
            "extra": "mean: 1.3443707547624582 usec\nrounds: 90572"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 192354.30573467337,
            "unit": "iter/sec",
            "range": "stddev: 8.929327381275533e-7",
            "extra": "mean: 5.198739878375085 usec\nrounds: 7385"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "1a8c0726f7c5313b520b50e1bde2a6bcab88f4f0",
          "message": "fix(drivers): use TYPE_CHECKING for CassandraDriver annotation in LazyDriver\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-01T16:57:52+02:00",
          "tree_id": "414b8f5d0615d112392aad1d39e9b81e727a6662",
          "url": "https://github.com/fruch/coodie/commit/1a8c0726f7c5313b520b50e1bde2a6bcab88f4f0"
        },
        "date": 1772377110905,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 52881.60452344085,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015679237710986524",
            "extra": "mean: 18.910167514995305 usec\nrounds: 8256"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 596538.9598152844,
            "unit": "iter/sec",
            "range": "stddev: 4.747269904994605e-7",
            "extra": "mean: 1.6763364463398094 usec\nrounds: 47758"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 623337.1712926677,
            "unit": "iter/sec",
            "range": "stddev: 3.8243468780857927e-7",
            "extra": "mean: 1.604268197139943 usec\nrounds: 50008"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 828819.4091067824,
            "unit": "iter/sec",
            "range": "stddev: 3.268722262096601e-7",
            "extra": "mean: 1.206535451525802 usec\nrounds: 166086"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 940866.3633379504,
            "unit": "iter/sec",
            "range": "stddev: 3.142446039415986e-7",
            "extra": "mean: 1.0628501973991915 usec\nrounds: 83036"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 728737.8541494667,
            "unit": "iter/sec",
            "range": "stddev: 3.440750220401399e-7",
            "extra": "mean: 1.372235563592524 usec\nrounds: 89929"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 188920.9987143108,
            "unit": "iter/sec",
            "range": "stddev: 7.561849241880971e-7",
            "extra": "mean: 5.293217836055457 usec\nrounds: 7726"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "5782481f1c4edb4ac6e9bbfcba87b2bf773ff46e",
          "message": "feat(document): warn on delete_columns() to recommend migration tools\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-01T17:00:50+02:00",
          "tree_id": "115969f5ebe63aec93c91c459ea0be9970701bf1",
          "url": "https://github.com/fruch/coodie/commit/5782481f1c4edb4ac6e9bbfcba87b2bf773ff46e"
        },
        "date": 1772377306576,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 52232.08288444545,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014947080712882553",
            "extra": "mean: 19.145321127865586 usec\nrounds: 8548"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 564697.5340983253,
            "unit": "iter/sec",
            "range": "stddev: 4.4009186736660625e-7",
            "extra": "mean: 1.7708595126003859 usec\nrounds: 35085"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 623380.9139354101,
            "unit": "iter/sec",
            "range": "stddev: 4.124352934078462e-7",
            "extra": "mean: 1.6041556256302263 usec\nrounds: 46599"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 849760.3510921572,
            "unit": "iter/sec",
            "range": "stddev: 3.4625102908993515e-7",
            "extra": "mean: 1.1768023757695294 usec\nrounds: 121139"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 889672.9953405734,
            "unit": "iter/sec",
            "range": "stddev: 3.237953163037356e-7",
            "extra": "mean: 1.124008489902734 usec\nrounds: 89518"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 748485.331630072,
            "unit": "iter/sec",
            "range": "stddev: 3.2835083093698715e-7",
            "extra": "mean: 1.3360315262587343 usec\nrounds: 91067"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 186132.15397671334,
            "unit": "iter/sec",
            "range": "stddev: 8.936828873110056e-7",
            "extra": "mean: 5.37252687746314 usec\nrounds: 7683"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "340979+fruch@users.noreply.github.com",
            "name": "fruch",
            "username": "fruch"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "f9f55c7b4a47578550e59000f1bc037dfddc98c2",
          "message": "test(integration): add CounterDocument integration tests\n\nAdd integration tests for CounterDocument covering increment, decrement,\nand read operations using a PageView model with view_count and unique_visitors\ncounter fields.\n\nFix NULL counter column handling: ScyllaDB returns NULL for counter columns that\nhave never been incremented.\nAdd field_validator(mode=\"before\") coercions on PageView to map None to 0,\npreventing Pydantic ValidationError on first read.",
          "timestamp": "2026-03-01T17:03:20+02:00",
          "tree_id": "43e740713805d234d1379cc6b4e19a42d10d91e4",
          "url": "https://github.com/fruch/coodie/commit/f9f55c7b4a47578550e59000f1bc037dfddc98c2"
        },
        "date": 1772377436614,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 53222.0545584822,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018905164995537486",
            "extra": "mean: 18.789203240945277 usec\nrounds: 7405"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 586360.1849221347,
            "unit": "iter/sec",
            "range": "stddev: 5.820199731341483e-7",
            "extra": "mean: 1.7054363950935623 usec\nrounds: 27773"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 597214.3188027679,
            "unit": "iter/sec",
            "range": "stddev: 6.183481875194252e-7",
            "extra": "mean: 1.674440763584996 usec\nrounds: 42170"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 833388.0828000807,
            "unit": "iter/sec",
            "range": "stddev: 3.8322563906480277e-7",
            "extra": "mean: 1.1999211659472306 usec\nrounds: 80828"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 915878.6143309516,
            "unit": "iter/sec",
            "range": "stddev: 2.894440994759837e-7",
            "extra": "mean: 1.0918477452718984 usec\nrounds: 33063"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 747382.5996869768,
            "unit": "iter/sec",
            "range": "stddev: 3.7770847508978585e-7",
            "extra": "mean: 1.3380027852117857 usec\nrounds: 85092"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 191139.69168389362,
            "unit": "iter/sec",
            "range": "stddev: 8.952133552983288e-7",
            "extra": "mean: 5.231775730044588 usec\nrounds: 7433"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "86c46d3557a6537693f9860b5252907622d32a5b",
          "message": "docs(perf): address code review feedback on Phase 8 plan\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-01T17:07:50+02:00",
          "tree_id": "755724341dfb83e75406bab03fb0cb2b47f24085",
          "url": "https://github.com/fruch/coodie/commit/86c46d3557a6537693f9860b5252907622d32a5b"
        },
        "date": 1772377705602,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 52255.14938465924,
            "unit": "iter/sec",
            "range": "stddev: 0.000001520399497910884",
            "extra": "mean: 19.136869988425946 usec\nrounds: 12122"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 581291.7923614106,
            "unit": "iter/sec",
            "range": "stddev: 4.453526851122246e-7",
            "extra": "mean: 1.7203064160559542 usec\nrounds: 52618"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 633371.4864631675,
            "unit": "iter/sec",
            "range": "stddev: 4.0459207400051924e-7",
            "extra": "mean: 1.5788522555445872 usec\nrounds: 60828"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 848513.2511111319,
            "unit": "iter/sec",
            "range": "stddev: 3.2917063129023106e-7",
            "extra": "mean: 1.1785319777746495 usec\nrounds: 160721"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 943477.7684108982,
            "unit": "iter/sec",
            "range": "stddev: 3.236004796838037e-7",
            "extra": "mean: 1.0599083873320114 usec\nrounds: 111895"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 732351.1210290306,
            "unit": "iter/sec",
            "range": "stddev: 3.661903635818382e-7",
            "extra": "mean: 1.3654652410375157 usec\nrounds: 146135"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 175896.59276116957,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019347662624785676",
            "extra": "mean: 5.68515844623431 usec\nrounds: 7826"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "59247b87faf5f5e6c50944e757299af410f8e308",
          "message": "docs(plans): add python-rs feature gap continuation plan\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-01T17:31:39+02:00",
          "tree_id": "c5fb2a2a85be8594ed7d80a5ac90e9b9eb38097a",
          "url": "https://github.com/fruch/coodie/commit/59247b87faf5f5e6c50944e757299af410f8e308"
        },
        "date": 1772379132328,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 51736.017878406376,
            "unit": "iter/sec",
            "range": "stddev: 0.000001632384479990541",
            "extra": "mean: 19.32889389265077 usec\nrounds: 8416"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 572666.7138630053,
            "unit": "iter/sec",
            "range": "stddev: 4.045494634489765e-7",
            "extra": "mean: 1.7462163869353553 usec\nrounds: 46708"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 600334.077612223,
            "unit": "iter/sec",
            "range": "stddev: 4.051826812261452e-7",
            "extra": "mean: 1.6657391897148561 usec\nrounds: 49097"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 852645.7294594548,
            "unit": "iter/sec",
            "range": "stddev: 3.595105958063172e-7",
            "extra": "mean: 1.1728200417234977 usec\nrounds: 157431"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 940572.4818162449,
            "unit": "iter/sec",
            "range": "stddev: 3.270003306857187e-7",
            "extra": "mean: 1.0631822845475987 usec\nrounds: 95329"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 747664.0863695389,
            "unit": "iter/sec",
            "range": "stddev: 3.934235440849078e-7",
            "extra": "mean: 1.3374990429936766 usec\nrounds: 87253"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 187374.10094020623,
            "unit": "iter/sec",
            "range": "stddev: 8.41647632102008e-7",
            "extra": "mean: 5.336916868351589 usec\nrounds: 7855"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "3270be1f6778c19e54120e0c037af2e33fa7c231",
          "message": "docs(plans): add Phase 8 benchmark analysis for §14.5.6 connection-level optimizations\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-01T17:31:59+02:00",
          "tree_id": "c388ddf70a585dcd8b56b0280fa0ddc2714e1813",
          "url": "https://github.com/fruch/coodie/commit/3270be1f6778c19e54120e0c037af2e33fa7c231"
        },
        "date": 1772379153168,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 52888.40067692174,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016472452390151062",
            "extra": "mean: 18.9077375606171 usec\nrounds: 8863"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 564736.8652429358,
            "unit": "iter/sec",
            "range": "stddev: 4.166472746670345e-7",
            "extra": "mean: 1.7707361809465454 usec\nrounds: 46729"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 597260.2790447605,
            "unit": "iter/sec",
            "range": "stddev: 3.8593036738446997e-7",
            "extra": "mean: 1.674311912386621 usec\nrounds: 57965"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 849714.9400719305,
            "unit": "iter/sec",
            "range": "stddev: 3.250501969853561e-7",
            "extra": "mean: 1.1768652672099038 usec\nrounds: 160206"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 956020.6457221261,
            "unit": "iter/sec",
            "range": "stddev: 3.2254067222883927e-7",
            "extra": "mean: 1.0460025151911383 usec\nrounds: 87866"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 755085.211770712,
            "unit": "iter/sec",
            "range": "stddev: 3.452202907330438e-7",
            "extra": "mean: 1.324353840349953 usec\nrounds: 135612"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 189004.6781305087,
            "unit": "iter/sec",
            "range": "stddev: 8.750847104489676e-7",
            "extra": "mean: 5.290874331213616 usec\nrounds: 7289"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "1498d812cf6b93f8829f94d717702fd11289f479",
          "message": "fix(pr-rebase-squash): add per-file timeout and diagnostics to resolve-conflicts.sh\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-01T17:49:01+02:00",
          "tree_id": "f1128588e465a93c7132a9f59bfc5e688444a23a",
          "url": "https://github.com/fruch/coodie/commit/1498d812cf6b93f8829f94d717702fd11289f479"
        },
        "date": 1772380180798,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 52449.14474239419,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018548545754789525",
            "extra": "mean: 19.066087824911826 usec\nrounds: 8460"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 584364.4331217055,
            "unit": "iter/sec",
            "range": "stddev: 4.793750450975233e-7",
            "extra": "mean: 1.7112608901571018 usec\nrounds: 37924"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 626864.0882246301,
            "unit": "iter/sec",
            "range": "stddev: 3.8170043139378235e-7",
            "extra": "mean: 1.5952421247038489 usec\nrounds: 46951"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 844137.5892957161,
            "unit": "iter/sec",
            "range": "stddev: 3.48112618478072e-7",
            "extra": "mean: 1.184641002463027 usec\nrounds: 152859"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 923919.4109149217,
            "unit": "iter/sec",
            "range": "stddev: 3.135937714459327e-7",
            "extra": "mean: 1.0823454818529452 usec\nrounds: 88488"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 741565.9200114657,
            "unit": "iter/sec",
            "range": "stddev: 3.5911958229345247e-7",
            "extra": "mean: 1.348497784235471 usec\nrounds: 89358"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 187668.82556130522,
            "unit": "iter/sec",
            "range": "stddev: 8.584223931982714e-7",
            "extra": "mean: 5.328535504013867 usec\nrounds: 7647"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "314e16e1209d105cca20395f3e0cff89446da728",
          "message": "ci: add pr-conflict-detect workflow for automatic conflict labeling\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-01T19:49:27+02:00",
          "tree_id": "a3f60b03a7d6fc96bd8fb4c7e8bf141f45e95fc2",
          "url": "https://github.com/fruch/coodie/commit/314e16e1209d105cca20395f3e0cff89446da728"
        },
        "date": 1772387405351,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 53050.1499753734,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016771094010985007",
            "extra": "mean: 18.850088085787004 usec\nrounds: 7084"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 574003.2331483685,
            "unit": "iter/sec",
            "range": "stddev: 4.6023452146165453e-7",
            "extra": "mean: 1.7421504657997626 usec\nrounds: 36819"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 600408.4722973567,
            "unit": "iter/sec",
            "range": "stddev: 5.510500361133284e-7",
            "extra": "mean: 1.6655327933226476 usec\nrounds: 39749"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 851931.2198444091,
            "unit": "iter/sec",
            "range": "stddev: 3.6550991597886267e-7",
            "extra": "mean: 1.1738036788728474 usec\nrounds: 96062"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 909996.8659895837,
            "unit": "iter/sec",
            "range": "stddev: 4.4129265388184774e-7",
            "extra": "mean: 1.0989048834937927 usec\nrounds: 82625"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 752316.3561567304,
            "unit": "iter/sec",
            "range": "stddev: 3.5489618923299656e-7",
            "extra": "mean: 1.329228045909545 usec\nrounds: 91828"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 191835.70577929035,
            "unit": "iter/sec",
            "range": "stddev: 7.544122730685813e-7",
            "extra": "mean: 5.212793916219716 usec\nrounds: 7594"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "02b04c757b7eb331f1331eca1531d9ab7fe9dfd2",
          "message": "docs(writing-plans): add pr-body-must-link-plan principle and AGENTS.md PR body convention\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-01T19:53:40+02:00",
          "tree_id": "ae0dab9e25ba3231efb6a8e1083704018b7329bd",
          "url": "https://github.com/fruch/coodie/commit/02b04c757b7eb331f1331eca1531d9ab7fe9dfd2"
        },
        "date": 1772387655714,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 52573.316757791676,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015163297334242478",
            "extra": "mean: 19.021055958996424 usec\nrounds: 8399"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 571407.4168208455,
            "unit": "iter/sec",
            "range": "stddev: 4.398349584853489e-7",
            "extra": "mean: 1.7500647883846632 usec\nrounds: 47987"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 618973.3215115191,
            "unit": "iter/sec",
            "range": "stddev: 3.8868810516938195e-7",
            "extra": "mean: 1.6155785156588367 usec\nrounds: 56199"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 836176.071252091,
            "unit": "iter/sec",
            "range": "stddev: 3.5153005108562545e-7",
            "extra": "mean: 1.1959203741654543 usec\nrounds: 160463"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 965380.504233107,
            "unit": "iter/sec",
            "range": "stddev: 3.030849084418016e-7",
            "extra": "mean: 1.0358609849847698 usec\nrounds: 89199"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 745610.1348274685,
            "unit": "iter/sec",
            "range": "stddev: 3.655159281433399e-7",
            "extra": "mean: 1.3411834862349294 usec\nrounds: 122625"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 189775.88833142855,
            "unit": "iter/sec",
            "range": "stddev: 8.523334204552649e-7",
            "extra": "mean: 5.269373305493789 usec\nrounds: 6713"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "340979+fruch@users.noreply.github.com",
            "name": "fruch",
            "username": "fruch"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "b73985fe72bd758cc33f1bc5959161dd53ca6b75",
          "message": "feat(migrations): phase C — makemigration, schema-diff, checksum validation\n\n  76c49a6 fc57185 2>/dev/null | head -60\n\nImplement Phase C of the migrations system: automatic schema diff and migration file generation.\n\nAdd `src/coodie/migrations/autogen.py` with `introspect_table`, `diff_schema`, `render_migration`, `next_migration_filename`, and `format_diff` — functions that compare a live keyspace against model definitions and produce ready-to-apply migration files. Extend `src/coodie/migrations/cli.py` with two new commands: `makemigration` (generates a migration file from detected schema drift) and `schema-diff` (prints a human-readable diff without writing files). Add checksum validation to `migrate --status` (Phase C.5). Export the new public API from `src/coodie/migrations/__init__.py`.\n\nCover the new functionality with 47 tests in `tests/test_migrations_autogen.py`, and add an API warning to `autogen.py` recommending the CLI over direct programmatic use. Follow-up commits apply ruff lint and format fixes.",
          "timestamp": "2026-03-01T20:09:14+02:00",
          "tree_id": "4993fc0286b402dd635dbd640e295e9d46562d82",
          "url": "https://github.com/fruch/coodie/commit/b73985fe72bd758cc33f1bc5959161dd53ca6b75"
        },
        "date": 1772388585213,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 52919.39552435561,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017788564842258363",
            "extra": "mean: 18.896663313921646 usec\nrounds: 9047"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 559169.3589327917,
            "unit": "iter/sec",
            "range": "stddev: 7.760483357608598e-7",
            "extra": "mean: 1.7883669482686966 usec\nrounds: 46993"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 628698.4111384748,
            "unit": "iter/sec",
            "range": "stddev: 3.741663370525594e-7",
            "extra": "mean: 1.59058776399507 usec\nrounds: 51422"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 812828.363761169,
            "unit": "iter/sec",
            "range": "stddev: 3.4819472642803475e-7",
            "extra": "mean: 1.2302720286146744 usec\nrounds: 152370"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 947612.4814778895,
            "unit": "iter/sec",
            "range": "stddev: 3.214118398766308e-7",
            "extra": "mean: 1.0552836940691277 usec\nrounds: 90654"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 734212.592443327,
            "unit": "iter/sec",
            "range": "stddev: 3.6458504512588983e-7",
            "extra": "mean: 1.3620033356717303 usec\nrounds: 98630"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 188026.70174587084,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010091682226003451",
            "extra": "mean: 5.318393561737624 usec\nrounds: 6741"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "d14bdea72f4ba825be8cddf26129d9217e1f64da",
          "message": "feat(demos): add lwt-user-registry demo showcasing LWT features\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-01T20:13:09+02:00",
          "tree_id": "2c64a9c9d833ea2d7d200c57df104d2b43b89665",
          "url": "https://github.com/fruch/coodie/commit/d14bdea72f4ba825be8cddf26129d9217e1f64da"
        },
        "date": 1772388823151,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 53513.70489646291,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016676819392970398",
            "extra": "mean: 18.686801856361413 usec\nrounds: 7757"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 570940.9886578344,
            "unit": "iter/sec",
            "range": "stddev: 4.507422950282335e-7",
            "extra": "mean: 1.7514944974449913 usec\nrounds: 38346"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 623047.014924876,
            "unit": "iter/sec",
            "range": "stddev: 4.533375651819311e-7",
            "extra": "mean: 1.6050153135242533 usec\nrounds: 47148"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 815133.5702890194,
            "unit": "iter/sec",
            "range": "stddev: 3.395663207230646e-7",
            "extra": "mean: 1.2267928060494837 usec\nrounds: 139005"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 930906.4651135795,
            "unit": "iter/sec",
            "range": "stddev: 3.032813557224866e-7",
            "extra": "mean: 1.0742217800345712 usec\nrounds: 86942"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 716310.8346346329,
            "unit": "iter/sec",
            "range": "stddev: 3.898842965223892e-7",
            "extra": "mean: 1.3960419857533886 usec\nrounds: 87101"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 181871.95011441017,
            "unit": "iter/sec",
            "range": "stddev: 8.857691436972651e-7",
            "extra": "mean: 5.498373989891955 usec\nrounds: 7797"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "63b7b70b779cb7cfef6758a455d96b9e8f27de25",
          "message": "fix(ci): filter standalone pipe commands from squash commit messages\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-01T20:35:54+02:00",
          "tree_id": "51d2ac2e4c441f423fb80504e95d27ec1b307713",
          "url": "https://github.com/fruch/coodie/commit/63b7b70b779cb7cfef6758a455d96b9e8f27de25"
        },
        "date": 1772390187289,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 80300.55220094579,
            "unit": "iter/sec",
            "range": "stddev: 8.229188484426411e-7",
            "extra": "mean: 12.453214487212728 usec\nrounds: 9222"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 588006.2735551555,
            "unit": "iter/sec",
            "range": "stddev: 2.5519843133264803e-7",
            "extra": "mean: 1.7006621272148708 usec\nrounds: 40166"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 684105.2719045905,
            "unit": "iter/sec",
            "range": "stddev: 2.4807646647115014e-7",
            "extra": "mean: 1.4617633295178962 usec\nrounds: 45088"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 954297.937943658,
            "unit": "iter/sec",
            "range": "stddev: 2.231169746807841e-7",
            "extra": "mean: 1.0478907689508603 usec\nrounds: 112880"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 1004176.1115574939,
            "unit": "iter/sec",
            "range": "stddev: 2.465253370152107e-7",
            "extra": "mean: 995.841255822132 nsec\nrounds: 92627"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 843522.4692337747,
            "unit": "iter/sec",
            "range": "stddev: 2.533702020480044e-7",
            "extra": "mean: 1.1855048756535957 usec\nrounds: 97628"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 192173.6126026872,
            "unit": "iter/sec",
            "range": "stddev: 4.964109121141446e-7",
            "extra": "mean: 5.203628044748621 usec\nrounds: 7759"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "9ca957e9cb5fae7c423943b8b91f71ecbcec50c8",
          "message": "ci: replace workflow_run with workflow_call to enable self-healing on bot PRs\n\nGitHub requires manual approval for workflow_run triggers initiated by bots (e.g., copilot-swe-agent).\nThis prevents the self-healing workflow from automatically commenting on failures in bot-authored PRs.\n\nSwitch to workflow_call pattern where each CI workflow directly invokes self-healing-ci.yml on failure.\nThis bypasses the approval requirement and enables automated failure analysis on all PRs regardless of author.\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-01T20:37:11+02:00",
          "tree_id": "dee798867b4f0dab00e29b3468c3828bbd8fd63b",
          "url": "https://github.com/fruch/coodie/commit/9ca957e9cb5fae7c423943b8b91f71ecbcec50c8"
        },
        "date": 1772390301389,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 51848.995529407075,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014423728428060329",
            "extra": "mean: 19.286776721312417 usec\nrounds: 8729"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 580904.6886515421,
            "unit": "iter/sec",
            "range": "stddev: 4.1285044716979895e-7",
            "extra": "mean: 1.7214527951587149 usec\nrounds: 51107"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 607872.8329289614,
            "unit": "iter/sec",
            "range": "stddev: 3.9090087081435433e-7",
            "extra": "mean: 1.6450809212539104 usec\nrounds: 54275"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 845865.2917401114,
            "unit": "iter/sec",
            "range": "stddev: 3.0148845442597577e-7",
            "extra": "mean: 1.1822213415836027 usec\nrounds: 156446"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 931942.9151260456,
            "unit": "iter/sec",
            "range": "stddev: 2.7921093130686856e-7",
            "extra": "mean: 1.073027096155079 usec\nrounds: 89127"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 749495.0212457273,
            "unit": "iter/sec",
            "range": "stddev: 3.7793068296068405e-7",
            "extra": "mean: 1.3342316782010255 usec\nrounds: 91735"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 186415.258977644,
            "unit": "iter/sec",
            "range": "stddev: 7.837505295402452e-7",
            "extra": "mean: 5.364367731935109 usec\nrounds: 7636"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "ad70fde49ee3117bbd081486343d6a7f2af7a2ea",
          "message": "fix(ci): add debug logging to mergeability retry loops\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-01T20:41:41+02:00",
          "tree_id": "810c2852f640b7156d7560be888a0b0835efab5a",
          "url": "https://github.com/fruch/coodie/commit/ad70fde49ee3117bbd081486343d6a7f2af7a2ea"
        },
        "date": 1772390540887,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 52415.74127690972,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016471683143346868",
            "extra": "mean: 19.078238247496117 usec\nrounds: 8445"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 553793.6069204608,
            "unit": "iter/sec",
            "range": "stddev: 5.361524500821206e-7",
            "extra": "mean: 1.805726876409438 usec\nrounds: 47484"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 597355.7069576435,
            "unit": "iter/sec",
            "range": "stddev: 4.122674669605967e-7",
            "extra": "mean: 1.6740444401092944 usec\nrounds: 46062"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 828010.1874624373,
            "unit": "iter/sec",
            "range": "stddev: 3.128578406304537e-7",
            "extra": "mean: 1.207714609242492 usec\nrounds: 132909"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 961252.0660881886,
            "unit": "iter/sec",
            "range": "stddev: 3.0119770416096353e-7",
            "extra": "mean: 1.0403098576104977 usec\nrounds: 91158"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 736823.2946319097,
            "unit": "iter/sec",
            "range": "stddev: 3.9893324803899905e-7",
            "extra": "mean: 1.3571775041389862 usec\nrounds: 96071"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 185522.5647588689,
            "unit": "iter/sec",
            "range": "stddev: 7.138901292353871e-7",
            "extra": "mean: 5.390179902373278 usec\nrounds: 7782"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "1552eaf606cf506506d3393faf746b116f2dd54d",
          "message": "refactor(ci): extract plan-continuation bash logic into testable scripts\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-01T21:06:26+02:00",
          "tree_id": "8495b7609bea4fb98affea10d3cad69ae2c7797e",
          "url": "https://github.com/fruch/coodie/commit/1552eaf606cf506506d3393faf746b116f2dd54d"
        },
        "date": 1772392023229,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 53073.62613094477,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016588478994382209",
            "extra": "mean: 18.841750091331072 usec\nrounds: 8211"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 580598.1070081921,
            "unit": "iter/sec",
            "range": "stddev: 4.204077939362872e-7",
            "extra": "mean: 1.7223617988576914 usec\nrounds: 47941"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 622434.0023313776,
            "unit": "iter/sec",
            "range": "stddev: 3.878435412855785e-7",
            "extra": "mean: 1.60659603468708 usec\nrounds: 36617"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 858881.0187186268,
            "unit": "iter/sec",
            "range": "stddev: 4.2649055699565103e-7",
            "extra": "mean: 1.1643056234866034 usec\nrounds: 156202"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 861473.0925287554,
            "unit": "iter/sec",
            "range": "stddev: 3.96662403457456e-7",
            "extra": "mean: 1.1608023612955976 usec\nrounds: 85970"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 758306.4751470898,
            "unit": "iter/sec",
            "range": "stddev: 3.307823997628483e-7",
            "extra": "mean: 1.3187280245840292 usec\nrounds: 87177"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 188447.8757991667,
            "unit": "iter/sec",
            "range": "stddev: 9.406202647087353e-7",
            "extra": "mean: 5.306507148245721 usec\nrounds: 7974"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "0e52104a73fe63aa4f0206f00d9f8ac2d1ff48ba",
          "message": "ci(solve): add /solve slash-command workflow and merge mode for resolve-conflicts.sh\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-01T21:27:52+02:00",
          "tree_id": "fd069af324ab9d2e52538cfe395e71ab9a1c775e",
          "url": "https://github.com/fruch/coodie/commit/0e52104a73fe63aa4f0206f00d9f8ac2d1ff48ba"
        },
        "date": 1772393304894,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 79182.253906755,
            "unit": "iter/sec",
            "range": "stddev: 9.567786689719974e-7",
            "extra": "mean: 12.629092387008834 usec\nrounds: 8919"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 589721.9156051526,
            "unit": "iter/sec",
            "range": "stddev: 3.3684876649658e-7",
            "extra": "mean: 1.6957144944729312 usec\nrounds: 38987"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 683226.6251371199,
            "unit": "iter/sec",
            "range": "stddev: 3.0613505085612564e-7",
            "extra": "mean: 1.4636431942319366 usec\nrounds: 40899"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 926254.6148989402,
            "unit": "iter/sec",
            "range": "stddev: 2.676092158548521e-7",
            "extra": "mean: 1.0796167532283831 usec\nrounds: 110498"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 958803.2150716445,
            "unit": "iter/sec",
            "range": "stddev: 2.959312485196844e-7",
            "extra": "mean: 1.0429668823391223 usec\nrounds: 88231"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 832909.0375356625,
            "unit": "iter/sec",
            "range": "stddev: 2.246351667801356e-7",
            "extra": "mean: 1.2006112971936425 usec\nrounds: 98785"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 191744.12192992575,
            "unit": "iter/sec",
            "range": "stddev: 6.16363681642948e-7",
            "extra": "mean: 5.215283733002554 usec\nrounds: 8004"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "07b8cd088aab499eac6e25c94c323859f8f04e5d",
          "message": "fix(drivers): route init_coodie_async acsylla+hosts path through AcsyllaDriver.connect\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-01T21:29:04+02:00",
          "tree_id": "e86f328367b64d1c1dddf00dacd655b4979a1e45",
          "url": "https://github.com/fruch/coodie/commit/07b8cd088aab499eac6e25c94c323859f8f04e5d"
        },
        "date": 1772393381378,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 52934.172428221165,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015326451904133775",
            "extra": "mean: 18.891388192684072 usec\nrounds: 8300"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 568744.2517023196,
            "unit": "iter/sec",
            "range": "stddev: 4.6042298245700806e-7",
            "extra": "mean: 1.758259528789751 usec\nrounds: 41348"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 620080.752536838,
            "unit": "iter/sec",
            "range": "stddev: 3.9015356718207593e-7",
            "extra": "mean: 1.6126931789268715 usec\nrounds: 46708"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 858464.098207029,
            "unit": "iter/sec",
            "range": "stddev: 3.585720886937857e-7",
            "extra": "mean: 1.1648710785792673 usec\nrounds: 155715"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 949476.0255394955,
            "unit": "iter/sec",
            "range": "stddev: 3.58857982737576e-7",
            "extra": "mean: 1.0532124804644714 usec\nrounds: 93458"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 746090.2342603243,
            "unit": "iter/sec",
            "range": "stddev: 3.3869874532380564e-7",
            "extra": "mean: 1.3403204519777725 usec\nrounds: 93546"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 192189.37512992622,
            "unit": "iter/sec",
            "range": "stddev: 7.667506198313833e-7",
            "extra": "mean: 5.203201266063577 usec\nrounds: 6792"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "1f4965710f30cd51a0d6b1dac52ac2bee155a37c",
          "message": "fix(test): use Optional field for TTL expiry test to ensure deterministic assertion\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-01T21:29:51+02:00",
          "tree_id": "c3d8ec5edb2dbb4759546e8e99dccf26824d8199",
          "url": "https://github.com/fruch/coodie/commit/1f4965710f30cd51a0d6b1dac52ac2bee155a37c"
        },
        "date": 1772393422957,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 52863.13320751823,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016626120759484038",
            "extra": "mean: 18.91677506277247 usec\nrounds: 8798"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 558218.930899193,
            "unit": "iter/sec",
            "range": "stddev: 5.66406712681293e-7",
            "extra": "mean: 1.7914118361933284 usec\nrounds: 44423"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 614579.0886664797,
            "unit": "iter/sec",
            "range": "stddev: 4.896792215774791e-7",
            "extra": "mean: 1.6271298819649245 usec\nrounds: 52925"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 813437.1505541544,
            "unit": "iter/sec",
            "range": "stddev: 3.776458655049957e-7",
            "extra": "mean: 1.2293512772544868 usec\nrounds: 149187"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 959472.5038313883,
            "unit": "iter/sec",
            "range": "stddev: 3.069995301903644e-7",
            "extra": "mean: 1.0422393513172876 usec\nrounds: 96256"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 755330.0899278978,
            "unit": "iter/sec",
            "range": "stddev: 3.2652053405842e-7",
            "extra": "mean: 1.323924484585882 usec\nrounds: 96722"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 190196.86096103344,
            "unit": "iter/sec",
            "range": "stddev: 7.708282428883849e-7",
            "extra": "mean: 5.257710326801213 usec\nrounds: 8047"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "b5932b31e932d3bec1aa59b3705394e003f9e480",
          "message": "fix(drivers): make _serialize_params fully recursive and fix empty-list handling\n\n- Add _serialize_param() helper that recursively handles lists, sets, tuples,\n  dicts and BaseModel instances\n- Fix execute_async() to use `if params else None` instead of `or None` to\n  avoid passing None when params is explicitly an empty list\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-01T21:30:55+02:00",
          "tree_id": "170e524c04188adfe439a09544558fa0b4b96708",
          "url": "https://github.com/fruch/coodie/commit/b5932b31e932d3bec1aa59b3705394e003f9e480"
        },
        "date": 1772393489603,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 52565.43738897823,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018816819355679006",
            "extra": "mean: 19.023907146441385 usec\nrounds: 8325"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 593181.6765537666,
            "unit": "iter/sec",
            "range": "stddev: 4.185147262535044e-7",
            "extra": "mean: 1.685824157296536 usec\nrounds: 43266"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 598440.8309477376,
            "unit": "iter/sec",
            "range": "stddev: 3.9194818414355037e-7",
            "extra": "mean: 1.6710089758018718 usec\nrounds: 47126"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 825937.1476286541,
            "unit": "iter/sec",
            "range": "stddev: 3.70494772063161e-7",
            "extra": "mean: 1.2107458816583045 usec\nrounds: 116064"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 848014.201237588,
            "unit": "iter/sec",
            "range": "stddev: 3.509731173482691e-7",
            "extra": "mean: 1.179225534832559 usec\nrounds: 78285"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 729118.6781182896,
            "unit": "iter/sec",
            "range": "stddev: 3.8946669036761724e-7",
            "extra": "mean: 1.3715188350143508 usec\nrounds: 87789"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 190461.99173040793,
            "unit": "iter/sec",
            "range": "stddev: 7.993884634674112e-7",
            "extra": "mean: 5.25039138210559 usec\nrounds: 6661"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "340979+fruch@users.noreply.github.com",
            "name": "fruch",
            "username": "fruch"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "19356ff91193a050f591b90baddf094ec06d88eb",
          "message": "feat(migrations): add data migration support (Phase D.1–D.4)\n\nAdd scan_table() to the migrations context object, enabling data migrations to iterate over all partitions in a table using token-range chunking.\n\nProgress is logged at 10% intervals. Callers can pass resume_token to skip ahead after a restart, and throttle_seconds to rate-limit between chunks. All behaviour is covered by 15 new unit tests.",
          "timestamp": "2026-03-01T21:39:38+02:00",
          "tree_id": "687ebceb03970610bfd210a5336680d3fdcfd429",
          "url": "https://github.com/fruch/coodie/commit/19356ff91193a050f591b90baddf094ec06d88eb"
        },
        "date": 1772394019961,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 52468.74736093493,
            "unit": "iter/sec",
            "range": "stddev: 0.000001744563498667509",
            "extra": "mean: 19.05896462747536 usec\nrounds: 12750"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 585342.7160215747,
            "unit": "iter/sec",
            "range": "stddev: 4.378035862251971e-7",
            "extra": "mean: 1.7084008609464647 usec\nrounds: 53894"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 594978.5895011561,
            "unit": "iter/sec",
            "range": "stddev: 4.296024599668182e-7",
            "extra": "mean: 1.6807327484480126 usec\nrounds: 58473"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 832821.4196862129,
            "unit": "iter/sec",
            "range": "stddev: 3.4150693648765624e-7",
            "extra": "mean: 1.2007376087622432 usec\nrounds: 157208"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 841941.9273432279,
            "unit": "iter/sec",
            "range": "stddev: 3.615951997814775e-7",
            "extra": "mean: 1.1877303737034794 usec\nrounds: 106770"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 715584.3364532088,
            "unit": "iter/sec",
            "range": "stddev: 5.355992549809413e-7",
            "extra": "mean: 1.397459319688992 usec\nrounds: 144259"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 184828.14452107318,
            "unit": "iter/sec",
            "range": "stddev: 9.784542882628036e-7",
            "extra": "mean: 5.4104314177432276 usec\nrounds: 7378"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "29139614+renovate[bot]@users.noreply.github.com",
            "name": "renovate[bot]",
            "username": "renovate[bot]"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "3db14da1552f3dc1ed31f377005a662f01addcd2",
          "message": "chore(deps): update dependency python to 3.14",
          "timestamp": "2026-03-02T07:11:39+02:00",
          "tree_id": "cd3a535285ecf021e40a8896d792476a0f7174ff",
          "url": "https://github.com/fruch/coodie/commit/3db14da1552f3dc1ed31f377005a662f01addcd2"
        },
        "date": 1772428339070,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 51875.33623410463,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019594750188907918",
            "extra": "mean: 19.276983487628282 usec\nrounds: 8660"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 582203.920022097,
            "unit": "iter/sec",
            "range": "stddev: 4.6552415479357123e-7",
            "extra": "mean: 1.717611245149373 usec\nrounds: 50901"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 619103.8624781687,
            "unit": "iter/sec",
            "range": "stddev: 4.12026980765235e-7",
            "extra": "mean: 1.6152378633161295 usec\nrounds: 61384"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 849897.6373343274,
            "unit": "iter/sec",
            "range": "stddev: 3.483989830639209e-7",
            "extra": "mean: 1.1766122837292066 usec\nrounds: 43684"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 875418.0954269572,
            "unit": "iter/sec",
            "range": "stddev: 3.7202016591334984e-7",
            "extra": "mean: 1.1423113198411576 usec\nrounds: 84948"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 740904.5460368415,
            "unit": "iter/sec",
            "range": "stddev: 3.7505110233226947e-7",
            "extra": "mean: 1.3497015308504734 usec\nrounds: 94787"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 190721.4333101375,
            "unit": "iter/sec",
            "range": "stddev: 8.929395201678899e-7",
            "extra": "mean: 5.243249186230012 usec\nrounds: 7677"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "29139614+renovate[bot]@users.noreply.github.com",
            "name": "renovate[bot]",
            "username": "renovate[bot]"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "37c5aefe176787c56cdc4d757d76641d4051cbf2",
          "message": "chore(deps): update actions/checkout action to v6",
          "timestamp": "2026-03-02T07:12:02+02:00",
          "tree_id": "fd955e5b17b89d126b16687a41afce45ab10fcf0",
          "url": "https://github.com/fruch/coodie/commit/37c5aefe176787c56cdc4d757d76641d4051cbf2"
        },
        "date": 1772428356815,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 44399.43788031128,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016189113446470567",
            "extra": "mean: 22.52280766922604 usec\nrounds: 6702"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 527623.0190299498,
            "unit": "iter/sec",
            "range": "stddev: 4.256481022972885e-7",
            "extra": "mean: 1.8952925932582112 usec\nrounds: 38627"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 603966.373871536,
            "unit": "iter/sec",
            "range": "stddev: 4.752450494867669e-7",
            "extra": "mean: 1.655721317049185 usec\nrounds: 41244"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 803810.4007417219,
            "unit": "iter/sec",
            "range": "stddev: 4.158467607391446e-7",
            "extra": "mean: 1.2440744721357708 usec\nrounds: 78996"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 799188.151593816,
            "unit": "iter/sec",
            "range": "stddev: 4.051028230731798e-7",
            "extra": "mean: 1.2512698017428139 usec\nrounds: 65007"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 676199.7683820651,
            "unit": "iter/sec",
            "range": "stddev: 4.2693599306853445e-7",
            "extra": "mean: 1.4788529170790574 usec\nrounds: 78126"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 180600.27024429536,
            "unit": "iter/sec",
            "range": "stddev: 8.225602652294939e-7",
            "extra": "mean: 5.537090274822482 usec\nrounds: 7311"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "bff0b33fa305dbec9f7c804780f934b555d9f70f",
          "message": "fix(ci): replace gh pr comment with gh api REST endpoint for fine-grained PAT compatibility\n\ngh pr comment uses the GitHub GraphQL API internally to resolve the PR,\nbut fine-grained PATs do NOT support the GitHub GraphQL API. This caused\nHTTP 401 errors, triggering the fallback to GITHUB_TOKEN, resulting in\ncomments posted by github-actions[bot] (which Copilot ignores).\n\nThe fix replaces gh pr comment with gh api --method POST to the REST\nendpoint (repos/{owner}/{repo}/issues/{n}/comments), which fine-grained\nPATs support. A jq step builds the JSON payload from the markdown file.\n\nUpdate the header comment to document this limitation clearly.\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-02T12:45:58+02:00",
          "tree_id": "64380b8859fd0335afd825d0a15b7a81dafab05e",
          "url": "https://github.com/fruch/coodie/commit/bff0b33fa305dbec9f7c804780f934b555d9f70f"
        },
        "date": 1772448398996,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 52582.72145541609,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015772025146033699",
            "extra": "mean: 19.01765394261462 usec\nrounds: 5999"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 569903.1195152837,
            "unit": "iter/sec",
            "range": "stddev: 5.191848505885116e-7",
            "extra": "mean: 1.7546842011507569 usec\nrounds: 28078"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 621318.3066664146,
            "unit": "iter/sec",
            "range": "stddev: 4.930822095802759e-7",
            "extra": "mean: 1.6094809846588014 usec\nrounds: 33473"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 826932.3387588052,
            "unit": "iter/sec",
            "range": "stddev: 4.1355947741999527e-7",
            "extra": "mean: 1.2092887811123254 usec\nrounds: 70943"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 880057.6969974743,
            "unit": "iter/sec",
            "range": "stddev: 7.512641491402097e-7",
            "extra": "mean: 1.1362891358279548 usec\nrounds: 58201"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 732212.439843893,
            "unit": "iter/sec",
            "range": "stddev: 3.783589943729462e-7",
            "extra": "mean: 1.3657238604320885 usec\nrounds: 69320"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 191350.5397932663,
            "unit": "iter/sec",
            "range": "stddev: 8.370798801035221e-7",
            "extra": "mean: 5.226010865087669 usec\nrounds: 7179"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "e9f03ae5e6a6d29a0ad137049f7fde6bceaffd30",
          "message": "fix(ci): move checkout step before script sourcing in plan-continuation workflow\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-02T12:46:29+02:00",
          "tree_id": "dc9d0606e4cc34f20bebcfae17f3d45595cd4f1d",
          "url": "https://github.com/fruch/coodie/commit/e9f03ae5e6a6d29a0ad137049f7fde6bceaffd30"
        },
        "date": 1772448424475,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 52248.88143606707,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015673837372680925",
            "extra": "mean: 19.13916571063101 usec\nrounds: 12552"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 561108.5560410954,
            "unit": "iter/sec",
            "range": "stddev: 4.594174946685918e-7",
            "extra": "mean: 1.7821863331678733 usec\nrounds: 56619"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 612745.7379632689,
            "unit": "iter/sec",
            "range": "stddev: 3.6570548314968786e-7",
            "extra": "mean: 1.6319982956126986 usec\nrounds: 62779"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 850876.6446745995,
            "unit": "iter/sec",
            "range": "stddev: 3.2059222446122575e-7",
            "extra": "mean: 1.1752584892989155 usec\nrounds: 160231"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 854692.1132344619,
            "unit": "iter/sec",
            "range": "stddev: 3.448356372042561e-7",
            "extra": "mean: 1.1700119663157307 usec\nrounds: 111396"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 740509.912276966,
            "unit": "iter/sec",
            "range": "stddev: 3.532211035707839e-7",
            "extra": "mean: 1.350420816009252 usec\nrounds: 151470"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 189387.48253872638,
            "unit": "iter/sec",
            "range": "stddev: 7.960983944306126e-7",
            "extra": "mean: 5.280180012929406 usec\nrounds: 7755"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "16b4f823e52464104fd5ba2d63ce37e20c6b2ae9",
          "message": "docs: add actual benchmark results (27/34 wins) to python-rs-driver plan\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-02T12:55:54+02:00",
          "tree_id": "7521b07d8c837e07f652cd8f7e1398b9832c9579",
          "url": "https://github.com/fruch/coodie/commit/16b4f823e52464104fd5ba2d63ce37e20c6b2ae9"
        },
        "date": 1772448992212,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 53369.645983156384,
            "unit": "iter/sec",
            "range": "stddev: 0.000001564711342919864",
            "extra": "mean: 18.73724252013219 usec\nrounds: 6952"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 581134.9705202067,
            "unit": "iter/sec",
            "range": "stddev: 4.931352561296888e-7",
            "extra": "mean: 1.7207706483484269 usec\nrounds: 40427"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 616816.7459883209,
            "unit": "iter/sec",
            "range": "stddev: 5.107948176296556e-7",
            "extra": "mean: 1.6212270605554127 usec\nrounds: 43059"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 808506.1853919415,
            "unit": "iter/sec",
            "range": "stddev: 4.693836289839252e-7",
            "extra": "mean: 1.236848917259956 usec\nrounds: 151930"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 867402.6714019304,
            "unit": "iter/sec",
            "range": "stddev: 3.8157026480735866e-7",
            "extra": "mean: 1.152867097335267 usec\nrounds: 68885"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 750202.1633501268,
            "unit": "iter/sec",
            "range": "stddev: 3.868441056533589e-7",
            "extra": "mean: 1.3329740286729752 usec\nrounds: 86942"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 188517.60103180975,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012257113190735382",
            "extra": "mean: 5.304544480338808 usec\nrounds: 6812"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "cb96ce02b9690492927a29490ddc1a0f8e23b436",
          "message": "docs(aio): document kwargs forwarding in AcsyllaDriver.connect_sync docstring\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-03T00:57:30+02:00",
          "tree_id": "790628d42af5888c05e3599dadf743c7a9cbe80d",
          "url": "https://github.com/fruch/coodie/commit/cb96ce02b9690492927a29490ddc1a0f8e23b436"
        },
        "date": 1772492289141,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 53875.620193534465,
            "unit": "iter/sec",
            "range": "stddev: 0.000001506929110579326",
            "extra": "mean: 18.56127124676717 usec\nrounds: 8413"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 587926.4591299571,
            "unit": "iter/sec",
            "range": "stddev: 4.5458467704698705e-7",
            "extra": "mean: 1.7008930019578468 usec\nrounds: 51057"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 599932.9240150126,
            "unit": "iter/sec",
            "range": "stddev: 4.540200301121287e-7",
            "extra": "mean: 1.6668530096790892 usec\nrounds: 49806"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 842145.4134116054,
            "unit": "iter/sec",
            "range": "stddev: 3.5833882670274167e-7",
            "extra": "mean: 1.1874433845681256 usec\nrounds: 42877"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 845596.5647287673,
            "unit": "iter/sec",
            "range": "stddev: 3.3324208694722936e-7",
            "extra": "mean: 1.1825970465250875 usec\nrounds: 99612"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 751411.5519099057,
            "unit": "iter/sec",
            "range": "stddev: 3.550066534701602e-7",
            "extra": "mean: 1.3308286217562701 usec\nrounds: 85676"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 190791.54769572467,
            "unit": "iter/sec",
            "range": "stddev: 6.454291684903427e-7",
            "extra": "mean: 5.241322333601513 usec\nrounds: 7576"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "f7738b5cf027b069659695fa8bfe851b87886421",
          "message": "fix(ci): remove GITHUB_TOKEN fallback in self-healing comment step\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-03T01:11:13+02:00",
          "tree_id": "037f9383090cd35551235cb7ade5b83a69956e64",
          "url": "https://github.com/fruch/coodie/commit/f7738b5cf027b069659695fa8bfe851b87886421"
        },
        "date": 1772493107273,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 52879.67880793842,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016126931475812787",
            "extra": "mean: 18.91085616522084 usec\nrounds: 8183"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 548368.6594011707,
            "unit": "iter/sec",
            "range": "stddev: 7.661861037632403e-7",
            "extra": "mean: 1.823590722876139 usec\nrounds: 50770"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 608764.0542959112,
            "unit": "iter/sec",
            "range": "stddev: 4.4274078266721774e-7",
            "extra": "mean: 1.6426725476696997 usec\nrounds: 59627"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 836051.6982152079,
            "unit": "iter/sec",
            "range": "stddev: 3.541175405393226e-7",
            "extra": "mean: 1.1960982821215325 usec\nrounds: 159439"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 862509.950159377,
            "unit": "iter/sec",
            "range": "stddev: 4.6292834398553025e-7",
            "extra": "mean: 1.1594069144538186 usec\nrounds: 73932"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 733691.3434392641,
            "unit": "iter/sec",
            "range": "stddev: 3.5388216445295617e-7",
            "extra": "mean: 1.3629709672086123 usec\nrounds: 110048"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 189346.31546086076,
            "unit": "iter/sec",
            "range": "stddev: 7.628594883569095e-7",
            "extra": "mean: 5.281328012990604 usec\nrounds: 7393"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "6b13fc3e9519e6ccaa4974a04f32628e0f9edca4",
          "message": "test(update): add LWTResult type assertions and existing-field check in if_conditions tests\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-03T20:19:25+02:00",
          "tree_id": "76179e6acc3ae9ed4ab00211e8216d1c80f6e3f6",
          "url": "https://github.com/fruch/coodie/commit/6b13fc3e9519e6ccaa4974a04f32628e0f9edca4"
        },
        "date": 1772562028901,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 52729.9988128604,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021264026227717525",
            "extra": "mean: 18.964536744046132 usec\nrounds: 7838"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 586711.8393736767,
            "unit": "iter/sec",
            "range": "stddev: 6.000531017516578e-7",
            "extra": "mean: 1.704414216470413 usec\nrounds: 30542"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 587983.2930291976,
            "unit": "iter/sec",
            "range": "stddev: 4.2728344625569913e-7",
            "extra": "mean: 1.7007285952771838 usec\nrounds: 41381"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 822926.2981636937,
            "unit": "iter/sec",
            "range": "stddev: 3.979029410168399e-7",
            "extra": "mean: 1.2151756508832379 usec\nrounds: 144030"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 835800.9515484398,
            "unit": "iter/sec",
            "range": "stddev: 3.213372669008378e-7",
            "extra": "mean: 1.1964571207383266 usec\nrounds: 33641"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 716246.6898986257,
            "unit": "iter/sec",
            "range": "stddev: 4.0728963594491485e-7",
            "extra": "mean: 1.396167010756497 usec\nrounds: 80887"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 190833.5328436941,
            "unit": "iter/sec",
            "range": "stddev: 8.399565885671679e-7",
            "extra": "mean: 5.240169194053906 usec\nrounds: 7122"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "0d82d5761a2e204d1e4aff9f18eea54db1d034c4",
          "message": "feat(ci): add Phase 4 safety gates to conflict detection and /solve workflows\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-03T20:19:47+02:00",
          "tree_id": "639040783cfa5b3b6962183762dee2a707fe5551",
          "url": "https://github.com/fruch/coodie/commit/0d82d5761a2e204d1e4aff9f18eea54db1d034c4"
        },
        "date": 1772562035742,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 53395.48497083636,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014799395432796862",
            "extra": "mean: 18.72817524826644 usec\nrounds: 8565"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 572754.2006044982,
            "unit": "iter/sec",
            "range": "stddev: 3.898080272417911e-7",
            "extra": "mean: 1.745949656841585 usec\nrounds: 45329"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 604107.9989650506,
            "unit": "iter/sec",
            "range": "stddev: 3.8006617834068337e-7",
            "extra": "mean: 1.6553331551861359 usec\nrounds: 54275"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 847497.9214521736,
            "unit": "iter/sec",
            "range": "stddev: 3.2050112296500027e-7",
            "extra": "mean: 1.179943896837548 usec\nrounds: 164447"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 852917.1487806727,
            "unit": "iter/sec",
            "range": "stddev: 3.612500919155154e-7",
            "extra": "mean: 1.1724468213936095 usec\nrounds: 75444"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 738348.767143755,
            "unit": "iter/sec",
            "range": "stddev: 3.400115177758587e-7",
            "extra": "mean: 1.3543734946134232 usec\nrounds: 100221"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 191728.7190263909,
            "unit": "iter/sec",
            "range": "stddev: 8.737876363218843e-7",
            "extra": "mean: 5.215702713073219 usec\nrounds: 7740"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "7118a521f118fec2995e454459b22049d7faaeac",
          "message": "feat(demos): randomize per-item TTL in seed.py with shorter default range (20–120s)\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-03T20:36:44+02:00",
          "tree_id": "a76d55fd9f4f45b919109ba328afb7a71d1c7c21",
          "url": "https://github.com/fruch/coodie/commit/7118a521f118fec2995e454459b22049d7faaeac"
        },
        "date": 1772563041774,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 52944.83142311242,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015926762648566185",
            "extra": "mean: 18.887584927949405 usec\nrounds: 8466"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 574518.4179586347,
            "unit": "iter/sec",
            "range": "stddev: 4.059566048368704e-7",
            "extra": "mean: 1.7405882365846104 usec\nrounds: 45123"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 598703.8948894065,
            "unit": "iter/sec",
            "range": "stddev: 3.84149908429858e-7",
            "extra": "mean: 1.6702747527385329 usec\nrounds: 48833"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 834443.2548204816,
            "unit": "iter/sec",
            "range": "stddev: 3.2392237721398445e-7",
            "extra": "mean: 1.1984038389945826 usec\nrounds: 139412"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 878614.1416087082,
            "unit": "iter/sec",
            "range": "stddev: 3.1007822921809766e-7",
            "extra": "mean: 1.1381560489898774 usec\nrounds: 78046"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 691222.9724872806,
            "unit": "iter/sec",
            "range": "stddev: 3.754502654711477e-7",
            "extra": "mean: 1.4467111768603744 usec\nrounds: 92593"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 174992.4696372946,
            "unit": "iter/sec",
            "range": "stddev: 7.633851766347271e-7",
            "extra": "mean: 5.714531614261411 usec\nrounds: 7718"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "fa3c42c2021e5618e7467b65f22c0581b5c9a97a",
          "message": "feat(demos): add materialized-views demo with product catalog, views, and HTMX UI\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-03T20:47:12+02:00",
          "tree_id": "89bf3b16206fefbe9814765e4b48d3f155d6744a",
          "url": "https://github.com/fruch/coodie/commit/fa3c42c2021e5618e7467b65f22c0581b5c9a97a"
        },
        "date": 1772563669076,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 53582.33203929453,
            "unit": "iter/sec",
            "range": "stddev: 0.000001667626594535082",
            "extra": "mean: 18.662868186973487 usec\nrounds: 8201"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 573121.6098464319,
            "unit": "iter/sec",
            "range": "stddev: 5.718253697552433e-7",
            "extra": "mean: 1.7448303864653618 usec\nrounds: 41229"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 627281.5258266086,
            "unit": "iter/sec",
            "range": "stddev: 3.7602624289661713e-7",
            "extra": "mean: 1.5941805374903024 usec\nrounds: 43304"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 829994.9960509032,
            "unit": "iter/sec",
            "range": "stddev: 4.1643695340755117e-7",
            "extra": "mean: 1.2048265408321455 usec\nrounds: 153304"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 862930.5605132567,
            "unit": "iter/sec",
            "range": "stddev: 3.471167193431733e-7",
            "extra": "mean: 1.1588417953412344 usec\nrounds: 75908"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 753278.8339505974,
            "unit": "iter/sec",
            "range": "stddev: 3.944346877013096e-7",
            "extra": "mean: 1.3275296675408554 usec\nrounds: 95694"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 190989.62947652306,
            "unit": "iter/sec",
            "range": "stddev: 8.766287019603632e-7",
            "extra": "mean: 5.235886381584517 usec\nrounds: 7446"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "015d6a566ac3cc5bd632c4d6f7d1a9504ed9eb86",
          "message": "feat(demos): add batch-importer demo showcasing BatchQuery with logged/unlogged batches\n\nDemonstrates practical use of coodie's BatchQuery feature for high-throughput\nCSV bulk imports into ScyllaDB. The demo is needed to provide users with a\nworking example of batch operations, comparing logged batches (atomic writes\nfor critical data) vs. unlogged batches (best-effort, higher throughput for logs).\n\nCode changes include a complete runnable demo with models (CargoEntry, ShipmentLog),\na CLI importer (seed.py) with rich progress bars, Makefile automation, sample CSV data,\nsmoke tests, and CI workflow integration.\n\nUsers can generate random cargo manifests or import CSV files,\nobserving batch performance differences in a practical scenario.\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-03T20:47:35+02:00",
          "tree_id": "c4b193726d8b2987e5dc8643bde9b484d3b00437",
          "url": "https://github.com/fruch/coodie/commit/015d6a566ac3cc5bd632c4d6f7d1a9504ed9eb86"
        },
        "date": 1772563702336,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 52685.4979061187,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015871281729231515",
            "extra": "mean: 18.980555176339404 usec\nrounds: 11427"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 575565.1568657045,
            "unit": "iter/sec",
            "range": "stddev: 5.588832813497102e-7",
            "extra": "mean: 1.7374227540902518 usec\nrounds: 56948"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 617472.5365377726,
            "unit": "iter/sec",
            "range": "stddev: 3.959922300837474e-7",
            "extra": "mean: 1.619505226268192 usec\nrounds: 65630"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 816873.612156259,
            "unit": "iter/sec",
            "range": "stddev: 3.354024635891688e-7",
            "extra": "mean: 1.2241795855791593 usec\nrounds: 159211"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 853404.3212344175,
            "unit": "iter/sec",
            "range": "stddev: 3.6295386413997203e-7",
            "extra": "mean: 1.171777521062393 usec\nrounds: 113831"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 732327.8447189296,
            "unit": "iter/sec",
            "range": "stddev: 3.5045661703587077e-7",
            "extra": "mean: 1.3655086409882504 usec\nrounds: 120993"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 190600.0513694594,
            "unit": "iter/sec",
            "range": "stddev: 7.201280344182404e-7",
            "extra": "mean: 5.2465883026526505 usec\nrounds: 7865"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "340979+fruch@users.noreply.github.com",
            "name": "fruch",
            "username": "fruch"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "ec0883255fa0c6fd830c110a7fab718d0aa96c0b",
          "message": "feat(drivers): upgrade PythonRsDriver to background-thread sync bridge\n\nUpgrade PythonRsDriver from using loop.run_until_complete() to a proper\nbackground-thread sync bridge, matching the pattern already used by\nAcsyllaDriver. The driver now starts a dedicated event loop on a daemon\nthread (_bg_loop / _bg_thread) and routes all synchronous calls through\nrun_coroutine_threadsafe(), eliminating the risk of blocking or nesting\nthe caller's event loop.\n\nRegister the python-rs driver in init_coodie() (sync path) so it can be\nused outside async contexts. Update the driver factory in __init__.py to\nhandle the new connect() classmethod signature.\n\nExtend the test suite with thread-safety assertions and explicit cleanup\nof the background thread after each test, preventing resource leaks\nbetween test runs.\n\nMark Phase 3 of sync-api-support.md as complete.",
          "timestamp": "2026-03-03T20:47:58+02:00",
          "tree_id": "28927af72d500375e59a2fdccd675cf3f9c05577",
          "url": "https://github.com/fruch/coodie/commit/ec0883255fa0c6fd830c110a7fab718d0aa96c0b"
        },
        "date": 1772563715364,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 53371.18937995285,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015089445229078474",
            "extra": "mean: 18.736700673483917 usec\nrounds: 8018"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 568133.3195231713,
            "unit": "iter/sec",
            "range": "stddev: 4.5904165499207043e-7",
            "extra": "mean: 1.7601502422693502 usec\nrounds: 31163"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 603759.903134639,
            "unit": "iter/sec",
            "range": "stddev: 3.8316311070161296e-7",
            "extra": "mean: 1.6562875321930732 usec\nrounds: 48172"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 834397.1003298404,
            "unit": "iter/sec",
            "range": "stddev: 3.499759184329117e-7",
            "extra": "mean: 1.1984701284372825 usec\nrounds: 156202"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 788578.2890851846,
            "unit": "iter/sec",
            "range": "stddev: 3.6063413702179653e-7",
            "extra": "mean: 1.2681049096090153 usec\nrounds: 86341"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 735867.1073808664,
            "unit": "iter/sec",
            "range": "stddev: 3.374678649249279e-7",
            "extra": "mean: 1.358941023412839 usec\nrounds: 99921"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 189337.8459191467,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010858653461710472",
            "extra": "mean: 5.28156425961998 usec\nrounds: 7672"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "86ece3281f01f665408ebfb92569c8fb651bb01d",
          "message": "fix(ci): add required-version to [tool.uv] in pyproject.toml for CI stability\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-03T23:55:44+02:00",
          "tree_id": "4999e0bbf0f9855ddb7c724b72409ae6918696e9",
          "url": "https://github.com/fruch/coodie/commit/86ece3281f01f665408ebfb92569c8fb651bb01d"
        },
        "date": 1772574983220,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 80231.58368411292,
            "unit": "iter/sec",
            "range": "stddev: 7.466497630773093e-7",
            "extra": "mean: 12.463919495060587 usec\nrounds: 8869"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 540399.7564099062,
            "unit": "iter/sec",
            "range": "stddev: 7.134723958318143e-7",
            "extra": "mean: 1.8504819592136823 usec\nrounds: 37914"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 639486.7445678782,
            "unit": "iter/sec",
            "range": "stddev: 2.659279490136173e-7",
            "extra": "mean: 1.5637540707364188 usec\nrounds: 43358"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 862829.7222079408,
            "unit": "iter/sec",
            "range": "stddev: 2.3789773771199253e-7",
            "extra": "mean: 1.1589772283702129 usec\nrounds: 109171"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 856018.4027006947,
            "unit": "iter/sec",
            "range": "stddev: 2.5737123242013274e-7",
            "extra": "mean: 1.1681991845561388 usec\nrounds: 79956"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 768977.778353083,
            "unit": "iter/sec",
            "range": "stddev: 2.493716253595397e-7",
            "extra": "mean: 1.3004276952471847 usec\nrounds: 93590"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 188434.61770290075,
            "unit": "iter/sec",
            "range": "stddev: 5.05134212487004e-7",
            "extra": "mean: 5.306880509486161 usec\nrounds: 7306"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "d72899191a07aac31b1de2a6d27b8787d69fbcbe",
          "message": "feat(types): add frozenset support and raise on unsupported schema types\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-03T23:57:20+02:00",
          "tree_id": "95730eb366bc831386022f0852f74b46faadecc0",
          "url": "https://github.com/fruch/coodie/commit/d72899191a07aac31b1de2a6d27b8787d69fbcbe"
        },
        "date": 1772575079911,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 53768.92644526059,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015933217085201556",
            "extra": "mean: 18.598102400613282 usec\nrounds: 7998"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 547463.1857680802,
            "unit": "iter/sec",
            "range": "stddev: 6.550145721145239e-7",
            "extra": "mean: 1.8266068404161635 usec\nrounds: 42044"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 579062.6239026127,
            "unit": "iter/sec",
            "range": "stddev: 4.363376565148302e-7",
            "extra": "mean: 1.7269289343188223 usec\nrounds: 45268"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 790798.1998657819,
            "unit": "iter/sec",
            "range": "stddev: 6.421501057656551e-7",
            "extra": "mean: 1.2645451142525674 usec\nrounds: 148523"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 876722.6400451765,
            "unit": "iter/sec",
            "range": "stddev: 3.215847093897274e-7",
            "extra": "mean: 1.140611584923222 usec\nrounds: 80432"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 707453.3993385407,
            "unit": "iter/sec",
            "range": "stddev: 3.585437171516462e-7",
            "extra": "mean: 1.4135206657215675 usec\nrounds: 92593"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 191029.76183169163,
            "unit": "iter/sec",
            "range": "stddev: 7.139449761319027e-7",
            "extra": "mean: 5.2347864040214755 usec\nrounds: 7767"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "340979+fruch@users.noreply.github.com",
            "name": "fruch",
            "username": "fruch"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "0ec061b561f3ee3485e5f54dae166b35fdb80dcc",
          "message": "ci: add copilot CI proxy workflow and repository_dispatch trigger\n\nBot-authored PRs (e.g. from `copilot-workspace[bot]`) cannot trigger GitHub Actions due to platform restrictions. This adds a proxy workflow pattern to bridge that gap.\n\n### Changes\n\n- **New `.github/workflows/copilot-ci-proxy.yml`**: Listens on `pull_request_target`, gates on bot authors (`copilot-workspace[bot]`, `github-actions[bot]`), and fires a `trigger-main-ci` repository dispatch via `peter-evans/repository-dispatch@v3` authenticated with `secrets.CI_DISPATCH_TOKEN`. Workflow-level `permissions: {}` since only the PAT is used.\n\n- **Updated `.github/workflows/ci.yml`**: Added `repository_dispatch` trigger restricted to `types: [trigger-main-ci]`. Existing `push`/`pull_request` triggers unchanged.\n\n- **Updated `.github/workflows/test-unit.yml`**: Added `repository_dispatch` trigger restricted to `types: [trigger-main-ci]`. Existing `push`/`pull_request` triggers unchanged.\n\n- **Updated `.github/workflows/test-integration.yml`**: Added `repository_dispatch` trigger restricted to `types: [trigger-main-ci]`. Existing `push`/`pull_request` triggers unchanged.\n\n- **Updated `.github/workflows/benchmark.yml`**: Added `repository_dispatch` trigger restricted to `types: [trigger-main-ci]`. Existing `push`/`pull_request`/`schedule` triggers unchanged. The existing `if` condition (`github.event_name != 'pull_request'`) naturally allows `repository_dispatch` events to proceed without requiring the `benchmark` label.\n\n### Flow\n\n```\nBot opens PR\n  → pull_request_target fires copilot-ci-proxy.yml\n    → repository-dispatch sends trigger-main-ci event\n      → ci.yml, test-unit.yml, test-integration.yml, and benchmark.yml all run as usual\n```\n\n<!-- START COPILOT CODING AGENT SUFFIX -->\n\n<!-- START COPILOT ORIGINAL PROMPT -->\n\n<details>\n\n<summary>Original prompt</summary>\n\n> I need to bypass GitHub's limitation where bots cannot trigger other GitHub Actions. I want to implement a 'Proxy Workflow' pattern. Please do the following two things:\n> Create a new GitHub Actions workflow file named copilot-ci-proxy.yml.\n> Set the trigger to on: pull_request_target.\n> Add a job that ONLY runs if the PR author is copilot-workspace[bot] (or github-actions[bot]).\n> In that job, use the peter-evans/repository-dispatch@v3 action to trigger a custom repository dispatch event called trigger-main-ci.\n> Authenticate this dispatch action using a secret called secrets.CI_DISPATCH_TOKEN.\n> Update my existing main CI workflow file (assume it's named ci.yml).\n> Keep the existing triggers, but add a new trigger for repository_dispatch.\n> Restrict the repository_dispatch trigger so it only listens for the trigger-main-ci event type.\n> Please output the exact YAML for the new proxy file, and show me the updated on: block for my existing CI file.\n\n</details>\n\n<!-- START COPILOT CODING AGENT TIPS -->\n---\n\n✨ Let Copilot coding agent [set things up for you](https://github.com/fruch/coodie/issues/new?title=✨+Set+up+Copilot+instructions&body=Configure%20instructions%20for%20this%20repository%20as%20documented%20in%20%5BBest%20practices%20for%20Copilot%20coding%20agent%20in%20your%20repository%5D%28https://gh.io/copilot-coding-agent-tips%29%2E%0A%0A%3COnboard%20this%20repo%3E&assignees=copilot) — coding agent works faster and does higher quality work when set up for your repo.",
          "timestamp": "2026-03-03T23:57:44+02:00",
          "tree_id": "b420880f1bd2b911e57b069bb6c13801a0bb1b58",
          "url": "https://github.com/fruch/coodie/commit/0ec061b561f3ee3485e5f54dae166b35fdb80dcc"
        },
        "date": 1772575096323,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 80029.53747727186,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010082820195970107",
            "extra": "mean: 12.495386472575788 usec\nrounds: 8782"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 590847.2404531104,
            "unit": "iter/sec",
            "range": "stddev: 2.934356729784319e-7",
            "extra": "mean: 1.6924848447004972 usec\nrounds: 46980"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 644617.8096080314,
            "unit": "iter/sec",
            "range": "stddev: 2.7277445435459503e-7",
            "extra": "mean: 1.5513068132698093 usec\nrounds: 45161"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 864429.8862387902,
            "unit": "iter/sec",
            "range": "stddev: 1.852295131841745e-7",
            "extra": "mean: 1.156831821665823 usec\nrounds: 114117"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 848007.2127192562,
            "unit": "iter/sec",
            "range": "stddev: 2.1781148048328067e-7",
            "extra": "mean: 1.1792352529565842 usec\nrounds: 74422"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 775819.7898775659,
            "unit": "iter/sec",
            "range": "stddev: 1.946139591889569e-7",
            "extra": "mean: 1.288959128198847 usec\nrounds: 91408"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 190660.51779954162,
            "unit": "iter/sec",
            "range": "stddev: 4.464964919209984e-7",
            "extra": "mean: 5.24492438991165 usec\nrounds: 7499"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "4d9c85de185390ad3c0fdcce5b5724b210557c61",
          "message": "feat(test): use PythonRsDriver.connect() in integration fixture and enable sync variant\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-04T00:32:30+02:00",
          "tree_id": "917eecb36feaff579634d1615a83f61b578d98d7",
          "url": "https://github.com/fruch/coodie/commit/4d9c85de185390ad3c0fdcce5b5724b210557c61"
        },
        "date": 1772577187865,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 53504.51364946626,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020644627767918394",
            "extra": "mean: 18.690011959579333 usec\nrounds: 8027"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 572580.2075692392,
            "unit": "iter/sec",
            "range": "stddev: 4.797958950214464e-7",
            "extra": "mean: 1.7464802079786788 usec\nrounds: 46534"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 605059.3667677498,
            "unit": "iter/sec",
            "range": "stddev: 3.8373609428427335e-7",
            "extra": "mean: 1.6527303846927253 usec\nrounds: 54014"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 829880.9201143002,
            "unit": "iter/sec",
            "range": "stddev: 3.2773703501464593e-7",
            "extra": "mean: 1.2049921570220812 usec\nrounds: 156446"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 826169.8012970119,
            "unit": "iter/sec",
            "range": "stddev: 3.7206458637859945e-7",
            "extra": "mean: 1.210404929386296 usec\nrounds: 76075"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 712454.1254398649,
            "unit": "iter/sec",
            "range": "stddev: 3.7033508761526873e-7",
            "extra": "mean: 1.4035991431484884 usec\nrounds: 105731"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 181548.57554508784,
            "unit": "iter/sec",
            "range": "stddev: 7.81982386407745e-7",
            "extra": "mean: 5.508167701110101 usec\nrounds: 7573"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "85c31c3f109b459503f5ee9a7da285079c68d732",
          "message": "test(ci): use mktemp for stderr capture files in bats tests\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-04T00:59:42+02:00",
          "tree_id": "8bbdd8eb461a3ca361cc90c9c1a5bcb5c067f75e",
          "url": "https://github.com/fruch/coodie/commit/85c31c3f109b459503f5ee9a7da285079c68d732"
        },
        "date": 1772578831803,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 52995.06421032915,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014801784924954306",
            "extra": "mean: 18.869681826049987 usec\nrounds: 11522"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 558144.3219570569,
            "unit": "iter/sec",
            "range": "stddev: 5.823907829150515e-7",
            "extra": "mean: 1.7916512999606202 usec\nrounds: 54425"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 602125.6938483268,
            "unit": "iter/sec",
            "range": "stddev: 4.5804130345586615e-7",
            "extra": "mean: 1.6607828070062332 usec\nrounds: 58303"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 849236.5052481398,
            "unit": "iter/sec",
            "range": "stddev: 3.3136682012198327e-7",
            "extra": "mean: 1.1775282784244046 usec\nrounds: 159185"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 866818.5816477058,
            "unit": "iter/sec",
            "range": "stddev: 3.544522824273116e-7",
            "extra": "mean: 1.1536439356193013 usec\nrounds: 37951"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 742308.8863485956,
            "unit": "iter/sec",
            "range": "stddev: 3.4838360714864333e-7",
            "extra": "mean: 1.3471480921089098 usec\nrounds: 142776"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 185690.25132189158,
            "unit": "iter/sec",
            "range": "stddev: 6.509243140417268e-7",
            "extra": "mean: 5.385312329975327 usec\nrounds: 6618"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "7ba91a3bb52e71dd1a9bc4badcf5463c7a0a974b",
          "message": "docs(skills): ensure pre-commit hooks are installed before any commits\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-04T01:00:04+02:00",
          "tree_id": "1f70eeac64d8ed9101988c3d8ea697e890d0ca51",
          "url": "https://github.com/fruch/coodie/commit/7ba91a3bb52e71dd1a9bc4badcf5463c7a0a974b"
        },
        "date": 1772578840429,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 53002.94932607363,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018481809654713737",
            "extra": "mean: 18.866874630843835 usec\nrounds: 8128"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 577146.165921072,
            "unit": "iter/sec",
            "range": "stddev: 4.1833711620820826e-7",
            "extra": "mean: 1.7326633339131559 usec\nrounds: 40907"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 609589.8153593054,
            "unit": "iter/sec",
            "range": "stddev: 4.893383418589532e-7",
            "extra": "mean: 1.6404473546044704 usec\nrounds: 41922"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 834448.774557648,
            "unit": "iter/sec",
            "range": "stddev: 3.284733271505792e-7",
            "extra": "mean: 1.1983959117563723 usec\nrounds: 136538"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 845563.8793909632,
            "unit": "iter/sec",
            "range": "stddev: 3.490475039478234e-7",
            "extra": "mean: 1.1826427599062923 usec\nrounds: 68321"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 730895.0895002867,
            "unit": "iter/sec",
            "range": "stddev: 3.563969790018145e-7",
            "extra": "mean: 1.3681854131537543 usec\nrounds: 89848"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 181967.08158860338,
            "unit": "iter/sec",
            "range": "stddev: 8.561120438797073e-7",
            "extra": "mean: 5.495499467650033 usec\nrounds: 7514"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "340979+fruch@users.noreply.github.com",
            "name": "fruch",
            "username": "fruch"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "83f226b2bdf9826999a87168b048345a762965d9",
          "message": "fix(ci): handle bad/expired GH_PAT gracefully in self-healing workflow\n\nSelf-healing CI workflow crashes with HTTP 401 when `GH_PAT` is set but expired/invalid. The existing check only tests for empty (`-z`), so a stale PAT passes validation then fails the `gh api` call, taking down the entire workflow.\n\n- **Fallback to `GITHUB_TOKEN`**: Try `GH_PAT` first; if it fails or is missing, post the CI failure comment with `GITHUB_TOKEN` instead\n- **Diagnostic comment on PAT failure**: When falling back, posts a separate ⚠️ comment via `GITHUB_TOKEN` explaining that `GH_PAT` is broken/not configured, warning that Copilot won't respond to bot-posted comments, and linking to setup documentation\n- **GH_PAT setup docs**: Added a new \"Self-Healing CI / `GH_PAT` Setup\" section to `CONTRIBUTING.md` with step-by-step instructions for creating a fine-grained PAT and storing it as the `GH_PAT` repository secret",
          "timestamp": "2026-03-04T23:00:47+02:00",
          "tree_id": "cc67165a54a423b9a3b8e6367c61956bb4abd961",
          "url": "https://github.com/fruch/coodie/commit/83f226b2bdf9826999a87168b048345a762965d9"
        },
        "date": 1772658088886,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 53761.66985027407,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017183801924853245",
            "extra": "mean: 18.60061271878262 usec\nrounds: 8397"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 549622.9114845592,
            "unit": "iter/sec",
            "range": "stddev: 7.380959264269423e-7",
            "extra": "mean: 1.819429247043122 usec\nrounds: 43136"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 603866.8807342688,
            "unit": "iter/sec",
            "range": "stddev: 4.112857223958577e-7",
            "extra": "mean: 1.6559941137756307 usec\nrounds: 45870"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 813624.6257705436,
            "unit": "iter/sec",
            "range": "stddev: 4.4458096201989974e-7",
            "extra": "mean: 1.2290680103898644 usec\nrounds: 154991"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 834337.1675115471,
            "unit": "iter/sec",
            "range": "stddev: 3.369086586356148e-7",
            "extra": "mean: 1.1985562179646758 usec\nrounds: 76488"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 726697.8928520603,
            "unit": "iter/sec",
            "range": "stddev: 3.3542494472331554e-7",
            "extra": "mean: 1.3760876560069757 usec\nrounds: 106975"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 187378.16903281608,
            "unit": "iter/sec",
            "range": "stddev: 6.778105046525463e-7",
            "extra": "mean: 5.336801000680432 usec\nrounds: 7794"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "914e8f8cb89313b93d9d9407d4d60aae18d09957",
          "message": "docs: add no-inline-imports rule to modern-python skill\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-04T23:07:42+02:00",
          "tree_id": "c9583d0918431368dbb168e93ec753fd0392f413",
          "url": "https://github.com/fruch/coodie/commit/914e8f8cb89313b93d9d9407d4d60aae18d09957"
        },
        "date": 1772658500023,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 53858.31219856965,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018839189479778128",
            "extra": "mean: 18.56723612713875 usec\nrounds: 6920"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 564749.8994929625,
            "unit": "iter/sec",
            "range": "stddev: 4.385648585384739e-7",
            "extra": "mean: 1.7706953129125103 usec\nrounds: 36270"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 586148.4963536698,
            "unit": "iter/sec",
            "range": "stddev: 6.049391899567289e-7",
            "extra": "mean: 1.7060523164707067 usec\nrounds: 46773"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 817681.665843989,
            "unit": "iter/sec",
            "range": "stddev: 3.656846792904033e-7",
            "extra": "mean: 1.2229698203735888 usec\nrounds: 140194"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 840841.4584311587,
            "unit": "iter/sec",
            "range": "stddev: 3.9971963248815813e-7",
            "extra": "mean: 1.189284840766295 usec\nrounds: 75393"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 723054.5861392922,
            "unit": "iter/sec",
            "range": "stddev: 4.5921545774371366e-7",
            "extra": "mean: 1.3830214470244102 usec\nrounds: 92507"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 188338.96167286596,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011408996966870379",
            "extra": "mean: 5.309575836660621 usec\nrounds: 6125"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "b74176fb93d2f3688249fc4dfa8c5e42878fbb7c",
          "message": "test(workflows): add Phase 5 Bats/convention tests, update CONTRIBUTING with /solve docs\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-04T23:11:10+02:00",
          "tree_id": "8f1ce484ab8d08e2ad24f76e1812886c87302c1b",
          "url": "https://github.com/fruch/coodie/commit/b74176fb93d2f3688249fc4dfa8c5e42878fbb7c"
        },
        "date": 1772658742669,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 53438.1010340502,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016228843347812802",
            "extra": "mean: 18.713239816714488 usec\nrounds: 7856"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 569432.4149859828,
            "unit": "iter/sec",
            "range": "stddev: 5.762030531567128e-7",
            "extra": "mean: 1.7561346591493499 usec\nrounds: 39173"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 585353.5745580568,
            "unit": "iter/sec",
            "range": "stddev: 4.977931718844819e-7",
            "extra": "mean: 1.708369169446009 usec\nrounds: 45001"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 822330.4243922401,
            "unit": "iter/sec",
            "range": "stddev: 3.421958611743748e-7",
            "extra": "mean: 1.2160561865859094 usec\nrounds: 142187"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 854172.3228061303,
            "unit": "iter/sec",
            "range": "stddev: 3.578009077158584e-7",
            "extra": "mean: 1.1707239549916533 usec\nrounds: 72749"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 725996.0097560451,
            "unit": "iter/sec",
            "range": "stddev: 3.846221727914959e-7",
            "extra": "mean: 1.3774180388898114 usec\nrounds: 88176"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 187510.83445275557,
            "unit": "iter/sec",
            "range": "stddev: 9.074227854905955e-7",
            "extra": "mean: 5.333025171150607 usec\nrounds: 4966"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "0ef64e207c8963e892fb7eee59b0ec02fc09b765",
          "message": "ci: disable subject-case commitlint rule for proper nouns and acronyms\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-04T23:22:52+02:00",
          "tree_id": "68364f894370982a3955f37d4fed196f1d47c6d5",
          "url": "https://github.com/fruch/coodie/commit/0ef64e207c8963e892fb7eee59b0ec02fc09b765"
        },
        "date": 1772659417595,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 53608.370588120866,
            "unit": "iter/sec",
            "range": "stddev: 0.000001530947258773129",
            "extra": "mean: 18.65380329656188 usec\nrounds: 8251"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 566409.1760593712,
            "unit": "iter/sec",
            "range": "stddev: 4.3355566491968e-7",
            "extra": "mean: 1.7655081207497592 usec\nrounds: 42730"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 592002.8484752682,
            "unit": "iter/sec",
            "range": "stddev: 4.288747024557745e-7",
            "extra": "mean: 1.6891810615025722 usec\nrounds: 51905"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 821719.6087151266,
            "unit": "iter/sec",
            "range": "stddev: 3.1141642781240643e-7",
            "extra": "mean: 1.2169601277540882 usec\nrounds: 152161"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 857523.9276197138,
            "unit": "iter/sec",
            "range": "stddev: 2.9694674472291024e-7",
            "extra": "mean: 1.166148217899606 usec\nrounds: 76482"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 740097.4038869654,
            "unit": "iter/sec",
            "range": "stddev: 3.692721091292333e-7",
            "extra": "mean: 1.3511735006068597 usec\nrounds: 69896"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 186483.3440352889,
            "unit": "iter/sec",
            "range": "stddev: 7.591943323395509e-7",
            "extra": "mean: 5.362409201600152 usec\nrounds: 7803"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "2c30872c9e2688c3ea28df0fb4b988b59f2dcc3b",
          "message": "ci: clarify alternatives — Copilot cannot be added as collaborator, add docs links\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-04T23:59:52+02:00",
          "tree_id": "61d74040efc357d3380243bfffc24061201d7a74",
          "url": "https://github.com/fruch/coodie/commit/2c30872c9e2688c3ea28df0fb4b988b59f2dcc3b"
        },
        "date": 1772661646652,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 53459.295871172595,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014922985252160605",
            "extra": "mean: 18.705820638001338 usec\nrounds: 8402"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 569687.4826984784,
            "unit": "iter/sec",
            "range": "stddev: 4.1179626726884654e-7",
            "extra": "mean: 1.755348380243902 usec\nrounds: 38524"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 606990.3831487738,
            "unit": "iter/sec",
            "range": "stddev: 4.0674736709249763e-7",
            "extra": "mean: 1.6474725593056048 usec\nrounds: 42765"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 791223.5015835818,
            "unit": "iter/sec",
            "range": "stddev: 5.373635907438524e-7",
            "extra": "mean: 1.2638653907506106 usec\nrounds: 153563"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 831722.8224559046,
            "unit": "iter/sec",
            "range": "stddev: 3.65247696226177e-7",
            "extra": "mean: 1.2023236263340806 usec\nrounds: 68885"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 711503.1112208222,
            "unit": "iter/sec",
            "range": "stddev: 3.459330791864728e-7",
            "extra": "mean: 1.4054752315617631 usec\nrounds: 93809"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 191779.5346080852,
            "unit": "iter/sec",
            "range": "stddev: 6.689365890594324e-7",
            "extra": "mean: 5.214320714895724 usec\nrounds: 6155"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "0e86df234aed24f12a6b422f2d2471b057e21df8",
          "message": "fix(ci): improve Copilot CLI observability and increase conflict resolution timeouts\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-05T00:04:11+02:00",
          "tree_id": "355094ea38e39d3a0ad753f0cdcd33868f4ed53b",
          "url": "https://github.com/fruch/coodie/commit/0e86df234aed24f12a6b422f2d2471b057e21df8"
        },
        "date": 1772661892254,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 53301.68058717087,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014431490767220373",
            "extra": "mean: 18.761134526791807 usec\nrounds: 7597"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 569887.3058976441,
            "unit": "iter/sec",
            "range": "stddev: 5.744015383005067e-7",
            "extra": "mean: 1.7547328913123874 usec\nrounds: 41178"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 619318.2629578641,
            "unit": "iter/sec",
            "range": "stddev: 4.4083425932106927e-7",
            "extra": "mean: 1.6146786875361947 usec\nrounds: 45227"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 816723.4381317112,
            "unit": "iter/sec",
            "range": "stddev: 3.6473374424647694e-7",
            "extra": "mean: 1.2244046801051058 usec\nrounds: 91067"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 840811.6876535717,
            "unit": "iter/sec",
            "range": "stddev: 3.393583945926761e-7",
            "extra": "mean: 1.1893269499983645 usec\nrounds: 74935"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 733093.138630093,
            "unit": "iter/sec",
            "range": "stddev: 4.7331148320606837e-7",
            "extra": "mean: 1.364083153020184 usec\nrounds: 90580"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 181417.14733976423,
            "unit": "iter/sec",
            "range": "stddev: 7.862730032459653e-7",
            "extra": "mean: 5.512158109989271 usec\nrounds: 7577"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "bf607acc17b3240d8bb1a58cedad2e364a91af60",
          "message": "ci: ensure Copilot CLI output is always visible in GitHub Actions logs\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-05T00:31:42+02:00",
          "tree_id": "339469894ab0e8b2e719c94eb9840764102efad1",
          "url": "https://github.com/fruch/coodie/commit/bf607acc17b3240d8bb1a58cedad2e364a91af60"
        },
        "date": 1772663540032,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 45254.7170879886,
            "unit": "iter/sec",
            "range": "stddev: 0.000001661779781606686",
            "extra": "mean: 22.097143996187253 usec\nrounds: 6521"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 534915.1254947687,
            "unit": "iter/sec",
            "range": "stddev: 5.08723531214434e-7",
            "extra": "mean: 1.8694554562745853 usec\nrounds: 33338"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 589390.7419628595,
            "unit": "iter/sec",
            "range": "stddev: 4.1380804090575357e-7",
            "extra": "mean: 1.6966673020171312 usec\nrounds: 38822"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 790764.3543089604,
            "unit": "iter/sec",
            "range": "stddev: 3.968447700828903e-7",
            "extra": "mean: 1.2645992381306668 usec\nrounds: 123123"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 827640.1378441631,
            "unit": "iter/sec",
            "range": "stddev: 3.85416305881059e-7",
            "extra": "mean: 1.2082545955356874 usec\nrounds: 70068"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 672586.294924749,
            "unit": "iter/sec",
            "range": "stddev: 3.9584225804409576e-7",
            "extra": "mean: 1.4867980622648327 usec\nrounds: 81847"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 176857.56826109652,
            "unit": "iter/sec",
            "range": "stddev: 7.483055233538775e-7",
            "extra": "mean: 5.6542674980337315 usec\nrounds: 6415"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "340979+fruch@users.noreply.github.com",
            "name": "fruch",
            "username": "fruch"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "6682e90497ebd8810c1d44aeea0e5c676d468ad3",
          "message": "fix(ci): use RUNNER_TEMP, avoid pre-creating Copilot output file, and add --add-dir to fix /tmp permission errors\n\n- [x] Fix Copilot /tmp permission issue in pr-rebase-squash.yml:\n  - [x] Replace `mktemp` (which pre-creates file in /tmp) with a deterministic path in `$RUNNER_TEMP` that is NOT pre-created\n  - [x] Add `--add-dir \"${RUNNER_TEMP}\"` to the `copilot -p` invocation to pre-authorize directory access\n  - [x] Add comprehensive debug output in pre/post validation groups\n  - [x] Fix shellcheck SC2015: replace `whoami && id || true` with `whoami; id`\n  - [x] Fix shellcheck SC2012: replace `ls -la /tmp/` with `find /tmp/ -maxdepth 1 -ls`\n  - [x] Fix shellcheck SC2012: replace `ls -la \"${RUNNER_TEMP}\"` with `find \"${RUNNER_TEMP}\" -maxdepth 1 -ls` in post-validation block\n\n<!-- START COPILOT CODING AGENT SUFFIX -->\n\n<!-- START COPILOT ORIGINAL PROMPT -->\n\n<details>\n\n<summary>Original prompt</summary>\n\n> copilot have premission issues with the file in /tmp\n>\n> https://github.com/fruch/coodie/actions/runs/22691557238/job/65788042447#step:14:123\n>\n> suggest other ways, and add debug print to understand what the permission situation with the file\n\n</details>\n\n<!-- START COPILOT CODING AGENT TIPS -->\n---\n\n💬 We'd love your input! Share your thoughts on Copilot coding agent in our [2 minute survey](https://gh.io/copilot-coding-agent-survey).",
          "timestamp": "2026-03-06T00:13:57+02:00",
          "tree_id": "b8e3b74876c04a8cfe6eb354c4640f29fd1234e9",
          "url": "https://github.com/fruch/coodie/commit/6682e90497ebd8810c1d44aeea0e5c676d468ad3"
        },
        "date": 1772748874107,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 53267.95254277705,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014859033636358497",
            "extra": "mean: 18.773013646374825 usec\nrounds: 7841"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 561129.6322982792,
            "unit": "iter/sec",
            "range": "stddev: 5.726326738575383e-7",
            "extra": "mean: 1.7821193935244377 usec\nrounds: 40957"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 617998.641903179,
            "unit": "iter/sec",
            "range": "stddev: 4.795866396561468e-7",
            "extra": "mean: 1.6181265332888364 usec\nrounds: 47039"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 830163.6786518687,
            "unit": "iter/sec",
            "range": "stddev: 3.3879879812248623e-7",
            "extra": "mean: 1.2045817297426626 usec\nrounds: 136725"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 841869.5010796832,
            "unit": "iter/sec",
            "range": "stddev: 3.244559007305182e-7",
            "extra": "mean: 1.1878325544725366 usec\nrounds: 72543"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 730347.2475030326,
            "unit": "iter/sec",
            "range": "stddev: 4.6722930419852054e-7",
            "extra": "mean: 1.3692117050059092 usec\nrounds: 100111"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 186767.71512552802,
            "unit": "iter/sec",
            "range": "stddev: 8.495310713478529e-7",
            "extra": "mean: 5.354244438488163 usec\nrounds: 7507"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "340979+fruch@users.noreply.github.com",
            "name": "fruch",
            "username": "fruch"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "9231257a9456a7225f916a125e897404f0cba1ec",
          "message": "fix(ci): replace raw log dumps in self-heal PR comments with deep-links\n\n- [x] Create `find-error-line.py` — parses a GitHub Actions job log and returns the 1-based line number of the first error within a given step (for deep-links like `#step:N:LM`)\n- [x] Update `collect-failed-logs.sh` — fetches job list once, downloads each log to a temp file, produces `FAILED_LINKS` (markdown deep-links) alongside `FAILED_LOGS` (still fed to AI summariser)\n- [x] Update `self-healing-ci.yml` — writes `FAILED_LINKS` to `/tmp/failed_links.txt`; replaces the `## Failed Job Logs` raw-dump section with a `### Failed Jobs` deep-link section\n- [x] Fix bats tests in `test_collect_failed_logs.bats` to match the new `gh` call pattern (script now fetches full JSON once, tests now mock the jobs endpoint to return proper JSON instead of jq-filtered text); also updated the \"no failed jobs\" mock to return `{\"jobs\":[]}` instead of empty string to prevent jq null-iteration errors\n- [x] All 69 bats tests pass locally\n\n<!-- START COPILOT CODING AGENT SUFFIX -->\n\n<!-- START COPILOT ORIGINAL PROMPT -->\n\n<details>\n\n<summary>Original prompt</summary>\n\n> self heal workflow shouldn't add logs in the comments only links into the failing action, with the exact line in the link if possible\n\n</details>\n\n<!-- START COPILOT CODING AGENT TIPS -->\n---\n\n💡 You can make Copilot smarter by setting up custom instructions, customizing its development environment and configuring Model Context Protocol (MCP) servers. Learn more [Copilot coding agent tips](https://gh.io/copilot-coding-agent-tips) in the docs.",
          "timestamp": "2026-03-06T00:29:48+02:00",
          "tree_id": "48877059244fd32dd7621b590ec907ecd9f9a45a",
          "url": "https://github.com/fruch/coodie/commit/9231257a9456a7225f916a125e897404f0cba1ec"
        },
        "date": 1772749826996,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 53828.81238564029,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018142358555465506",
            "extra": "mean: 18.577411532615685 usec\nrounds: 9625"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 585709.7958454955,
            "unit": "iter/sec",
            "range": "stddev: 4.1899445535098804e-7",
            "extra": "mean: 1.7073301609314215 usec\nrounds: 53377"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 610727.2849539518,
            "unit": "iter/sec",
            "range": "stddev: 4.4133716845861646e-7",
            "extra": "mean: 1.6373920481961093 usec\nrounds: 62074"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 822742.9207528948,
            "unit": "iter/sec",
            "range": "stddev: 3.429999207811923e-7",
            "extra": "mean: 1.2154464958323756 usec\nrounds: 157184"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 870087.293001997,
            "unit": "iter/sec",
            "range": "stddev: 3.1530358258983107e-7",
            "extra": "mean: 1.1493099692902937 usec\nrounds: 84660"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 717780.083874507,
            "unit": "iter/sec",
            "range": "stddev: 4.0456319398217293e-7",
            "extra": "mean: 1.393184378427021 usec\nrounds: 124456"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 188929.440074224,
            "unit": "iter/sec",
            "range": "stddev: 8.174707365337726e-7",
            "extra": "mean: 5.29298133529181 usec\nrounds: 7340"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "4a64b049d34ece6cd02685047d08b0c7865764eb",
          "message": "docs(plans): fix task reference format consistency in Phase 9 priority matrix\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-06T11:09:14+02:00",
          "tree_id": "16dabc1b7eef5c3f00f4132ebb53e01a790141f6",
          "url": "https://github.com/fruch/coodie/commit/4a64b049d34ece6cd02685047d08b0c7865764eb"
        },
        "date": 1772788190371,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 54111.84238742188,
            "unit": "iter/sec",
            "range": "stddev: 0.000001882251750264234",
            "extra": "mean: 18.480243064731553 usec\nrounds: 7570"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 577242.1541511774,
            "unit": "iter/sec",
            "range": "stddev: 4.035429011518748e-7",
            "extra": "mean: 1.7323752134327046 usec\nrounds: 38658"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 618910.9009551514,
            "unit": "iter/sec",
            "range": "stddev: 3.85476238646271e-7",
            "extra": "mean: 1.615741455606489 usec\nrounds: 43625"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 781395.6500343796,
            "unit": "iter/sec",
            "range": "stddev: 4.6560236695644106e-7",
            "extra": "mean: 1.279761411464221 usec\nrounds: 149433"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 842518.3162262302,
            "unit": "iter/sec",
            "range": "stddev: 3.810491436948436e-7",
            "extra": "mean: 1.1869178161955631 usec\nrounds: 70537"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 710206.870919967,
            "unit": "iter/sec",
            "range": "stddev: 3.633979879371712e-7",
            "extra": "mean: 1.408040447010389 usec\nrounds: 90736"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 182557.87390904865,
            "unit": "iter/sec",
            "range": "stddev: 0.000001030877714312707",
            "extra": "mean: 5.477714976556999 usec\nrounds: 7238"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "340979+fruch@users.noreply.github.com",
            "name": "fruch",
            "username": "fruch"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "fa041013c9cf1d5ab77306bf23298e36b817141b",
          "message": "fix(ci): replace Copilot CLI with GitHub Models API for squash/conflict resolution\n\nCopilot CLI's permission sandbox blocks file writes, `python3`, `gh`, and most commands in CI with \"Permission denied and could not request permission from user\". The `--add-dir` workaround doesn't help — the sandbox restricts general bash operations, not just directory access. Every `/squash` and `/rebase` invocation silently falls back to defaults.\n\nReplace all `copilot -p` usage with direct GitHub Models API calls — the same pattern `summarize-failure.py` already uses successfully in self-healing CI.\n\n### New scripts\n- **`generate-squash-body.py`** — Models API → commit body from log + diff stat\n- **`resolve-conflict-file.py`** — Models API → resolved file content from conflicted file\n\n### Workflow changes (`pr-rebase-squash.yml`, `pr-solve-command.yml`)\n- Add `models: read` permission\n- Replace `npm install -g @github/copilot` + `copilot -p` with `python3` script calls\n- Remove `COPILOT_PAT` / `COPILOT_GITHUB_TOKEN` env vars and the COPILOT_PAT guard step\n- Remove all pre/post file-validation debug blocks (no longer needed)\n\n### `resolve-conflicts.sh`\n- Calls `python3 \"$SCRIPT_DIR/resolve-conflict-file.py\" --file \"$FILE\" --output-file \"$RESOLVE_OUTFILE\"` instead of `copilot -p`\n- Env var renamed: `COPILOT_TIMEOUT` → `RESOLVE_TIMEOUT` (default 120s, down from 300s)\n\n### Tests\n- 17 new pytest tests for both scripts (mirrors `test_summarize_failure.py` structure)\n- Updated `test_resolve_conflicts.bats` — mocks `python3` instead of `copilot` binary\n- All 69 bats + 95 pytest workflow tests pass\n\n<!-- START COPILOT CODING AGENT TIPS -->\n---\n\n💡 You can make Copilot smarter by setting up custom instructions, customizing its development environment and configuring Model Context Protocol (MCP) servers. Learn more [Copilot coding agent tips](https://gh.io/copilot-coding-agent-tips) in the docs.",
          "timestamp": "2026-03-06T11:10:43+02:00",
          "tree_id": "b91916e996542a0f770f0f8147c92c2554e22718",
          "url": "https://github.com/fruch/coodie/commit/fa041013c9cf1d5ab77306bf23298e36b817141b"
        },
        "date": 1772788313583,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 52305.22910673494,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019071499391480484",
            "extra": "mean: 19.11854736281497 usec\nrounds: 7527"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 535222.1282964675,
            "unit": "iter/sec",
            "range": "stddev: 4.968708567110779e-7",
            "extra": "mean: 1.8683831387593248 usec\nrounds: 50744"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 599550.9797116412,
            "unit": "iter/sec",
            "range": "stddev: 4.539964247539163e-7",
            "extra": "mean: 1.6679148793668186 usec\nrounds: 46252"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 828219.6286043419,
            "unit": "iter/sec",
            "range": "stddev: 3.384036406641201e-7",
            "extra": "mean: 1.2074092009689874 usec\nrounds: 156962"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 860349.0865193552,
            "unit": "iter/sec",
            "range": "stddev: 3.3040848997956256e-7",
            "extra": "mean: 1.1623188955144002 usec\nrounds: 76605"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 746183.858720753,
            "unit": "iter/sec",
            "range": "stddev: 3.9461244245156536e-7",
            "extra": "mean: 1.3401522805845545 usec\nrounds: 100919"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 186691.1394605249,
            "unit": "iter/sec",
            "range": "stddev: 7.698450402405646e-7",
            "extra": "mean: 5.356440604999607 usec\nrounds: 7408"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "340979+fruch@users.noreply.github.com",
            "name": "fruch",
            "username": "fruch"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "da9167e7f3112a5d05d3b6e612242d561f7203ce",
          "message": "feat: improve self-heal flow with smart snippet extraction and PR check inspection\n\nEnhanced the self-heal flow by adding scripts for log snippet extraction and PR check inspection. Refined existing code based on review feedback and included comprehensive tests for new functionality, improving the reliability and clarity of the self-heal process.",
          "timestamp": "2026-03-08T00:01:19+02:00",
          "tree_id": "e9053f391e49b8458ed0581ee4935c50ec847294",
          "url": "https://github.com/fruch/coodie/commit/da9167e7f3112a5d05d3b6e612242d561f7203ce"
        },
        "date": 1772920916170,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 80760.71983258119,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012083990061367684",
            "extra": "mean: 12.382257142742446 usec\nrounds: 8225"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 573656.8904952756,
            "unit": "iter/sec",
            "range": "stddev: 2.730346431486639e-7",
            "extra": "mean: 1.7432022809603742 usec\nrounds: 24901"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 642698.927595499,
            "unit": "iter/sec",
            "range": "stddev: 3.463507512647569e-7",
            "extra": "mean: 1.5559384916686507 usec\nrounds: 44433"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 887236.1492029276,
            "unit": "iter/sec",
            "range": "stddev: 2.905280238561601e-7",
            "extra": "mean: 1.127095645165469 usec\nrounds: 97088"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 843447.6899753623,
            "unit": "iter/sec",
            "range": "stddev: 2.6519801427703225e-7",
            "extra": "mean: 1.1856099813720646 usec\nrounds: 74058"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 796289.9356278784,
            "unit": "iter/sec",
            "range": "stddev: 2.6357174934971647e-7",
            "extra": "mean: 1.2558239847794825 usec\nrounds: 80084"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 194068.73710197792,
            "unit": "iter/sec",
            "range": "stddev: 4.746981684024983e-7",
            "extra": "mean: 5.152813456371011 usec\nrounds: 7580"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "e4be2755c0585a7568d0259c46c173df9fe78db7",
          "message": "docs(skills): add example prompts section to code-review SKILL.md\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-08T00:01:57+02:00",
          "tree_id": "8fcd477009e935e15a36d0b7ead269640b04146b",
          "url": "https://github.com/fruch/coodie/commit/e4be2755c0585a7568d0259c46c173df9fe78db7"
        },
        "date": 1772920951839,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 52947.953058411185,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017172484799832793",
            "extra": "mean: 18.886471378729578 usec\nrounds: 8333"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 579803.3122466741,
            "unit": "iter/sec",
            "range": "stddev: 4.6481012160885253e-7",
            "extra": "mean: 1.7247228135436306 usec\nrounds: 50641"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 612239.4987879124,
            "unit": "iter/sec",
            "range": "stddev: 3.50198330400599e-7",
            "extra": "mean: 1.6333477372494922 usec\nrounds: 54337"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 811650.8552487771,
            "unit": "iter/sec",
            "range": "stddev: 3.5420923750059253e-7",
            "extra": "mean: 1.2320568549065256 usec\nrounds: 149433"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 856493.5790591607,
            "unit": "iter/sec",
            "range": "stddev: 3.451889801111353e-7",
            "extra": "mean: 1.167551076212945 usec\nrounds: 78285"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 718520.4460588612,
            "unit": "iter/sec",
            "range": "stddev: 3.581261408882907e-7",
            "extra": "mean: 1.3917488437316925 usec\nrounds: 102271"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 189309.85923503866,
            "unit": "iter/sec",
            "range": "stddev: 8.028719798561412e-7",
            "extra": "mean: 5.282345061376041 usec\nrounds: 6196"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "340979+fruch@users.noreply.github.com",
            "name": "fruch",
            "username": "fruch"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "762eae4f2966bb2fe4c7289cdb02cd982f2f09e6",
          "message": "feat(benchmarks): add Raw+DC benchmarks — dataclasses + raw CQL baseline\n\nAdds a third benchmark contender — **Raw+DC** (Python `dataclasses` + hand-written CQL with prepared statements) — inspired by [mkennedy's Raw+DC pattern](https://mkennedy.codes/posts/raw-dc-the-orm-pattern-of-2026/). This establishes the performance floor against which both coodie and cqlengine ORM overhead is measured.\n\n### Changes\n\n- **`benchmarks/models_raw_dc.py`** — `@dataclass` equivalents of Product, Review, Event\n- **`benchmarks/bench_raw_dc.py`** — 20 benchmarks covering every existing group: INSERT (single/INE/TTL), GET by PK, filter (index/limit), COUNT, UPDATE (partial/LWT), DELETE (single/bulk), batch (10/100), collection read/write/roundtrip, model instantiation, serialization\n- **`benchmarks/conftest.py`** — docstring updates; `bench_env` unchanged (Raw+DC lazily prepares its own statements via `cql_session`)\n- **`benchmarks/README.md`** — updated for three-way comparison\n- **`docs/plans/raw-dc-benchmark-plan.md`** — plan document with benchmark results analysis and key takeaways\n\nAll Raw+DC tests join the same `@pytest.mark.benchmark(group=...)` groups, so `--benchmark-group-by=group` shows all three contenders side by side:\n\n```bash\npytest benchmarks/ -v --benchmark-enable --benchmark-group-by=group\n```\n\n### Benchmark Results Summary (CI Run #22739849451)\n\n| Category | coodie vs Raw+DC Overhead |\n|---|---|\n| **CRUD writes** (insert, delete, bulk-delete) | **1.00–1.06×** — near-zero overhead |\n| **CRUD reads** (get-by-pk, filter-limit, collections) | **1.06–1.13×** — very low overhead |\n| **Batch-100 inserts** | **0.05×** 🚀 — coodie 21× faster (native BATCH vs manual loop) |\n| **Model serialization** | **0.20×** 🚀 — Pydantic `model_dump()` 5× faster than `dataclasses.asdict()` |\n| **Filter-secondary-index** | **2.00×** — multi-row hydration overhead |\n| **Partial update** | **2.35×** — change-tracking + validation cost |\n| **Model instantiation** | **3.01×** — Pydantic validation vs plain dataclass |\n\nKey design choices: prepared statements lazily cached at module level (single source of truth), reuses existing tables created by cqlengine/coodie fixtures, `_row_to_product()` hydrates driver `Row` → dataclass using dict key access (since coodie's CassandraDriver sets `dict_factory` on the shared session).\n\nPlan: docs/plans/raw-dc-benchmark-plan.md\nPhase: 1\n\n<!-- START COPILOT CODING AGENT TIPS -->\n---\n\n🔒 GitHub Advanced Security automatically protects Copilot coding agent pull requests. You can protect all pull requests by enabling Advanced Security for your repositories. [Learn more about Advanced Security.](https://gh.io/cca-advanced-security)",
          "timestamp": "2026-03-08T00:07:52+02:00",
          "tree_id": "f83f7730c77f19e2ff68469de4168cecbe90146e",
          "url": "https://github.com/fruch/coodie/commit/762eae4f2966bb2fe4c7289cdb02cd982f2f09e6"
        },
        "date": 1772921305462,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 53052.422602062674,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021278922100572297",
            "extra": "mean: 18.849280597435342 usec\nrounds: 7648"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_instantiation",
            "value": 1722029.9398174053,
            "unit": "iter/sec",
            "range": "stddev: 2.2018838496540594e-7",
            "extra": "mean: 580.7099963116987 nsec\nrounds: 192308"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_serialization",
            "value": 153845.7996304958,
            "unit": "iter/sec",
            "range": "stddev: 0.000008864374839159891",
            "extra": "mean: 6.500014965646009 usec\nrounds: 14300"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 553628.9655497108,
            "unit": "iter/sec",
            "range": "stddev: 4.4780582933960764e-7",
            "extra": "mean: 1.8062638738691668 usec\nrounds: 43229"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 610244.58902823,
            "unit": "iter/sec",
            "range": "stddev: 4.3427848459783887e-7",
            "extra": "mean: 1.6386872050638368 usec\nrounds: 44323"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 836522.3661366262,
            "unit": "iter/sec",
            "range": "stddev: 2.9864573689023383e-7",
            "extra": "mean: 1.1954252994075636 usec\nrounds: 149410"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 820457.8260997648,
            "unit": "iter/sec",
            "range": "stddev: 3.244565765419018e-7",
            "extra": "mean: 1.2188316915126889 usec\nrounds: 76841"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 729567.8695300232,
            "unit": "iter/sec",
            "range": "stddev: 3.3870859033240396e-7",
            "extra": "mean: 1.3706743974953082 usec\nrounds: 95248"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 190557.6389985334,
            "unit": "iter/sec",
            "range": "stddev: 7.821578029787203e-7",
            "extra": "mean: 5.247756034633156 usec\nrounds: 7665"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "340979+fruch@users.noreply.github.com",
            "name": "fruch",
            "username": "fruch"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "b07f1cd6f693478a9e460e61ed7e4551d0eb4588",
          "message": "feat(cql_builder): implement Phase 1 DML gaps — TRUNCATE, DISTINCT, GROUP BY, aggregates, IS NOT NULL, CAST, TOKEN\n\nCloses the highest-priority DML gaps identified in `docs/plans/cql-gap-analysis.md` Phase 1.\n\n### CQL builder (`cql_builder.py`)\n- `build_truncate(table, keyspace)` — `TRUNCATE TABLE`\n- `build_aggregate(table, keyspace, func, column, ...)` — `SELECT SUM/AVG/MIN/MAX`\n- `build_select()` extended with `distinct`, `group_by`, `select_token`, `cast` params\n- `parse_filter_kwargs()` gains `__isnull` operator; `build_where_clause()` emits `IS [NOT] NULL` (no bind params, value baked into cache key)\n\n### Document (`aio/document.py`, `sync/document.py`)\n- `Document.truncate()` classmethod (async + sync)\n\n### QuerySet (`aio/query.py`, `sync/query.py`)\n- **Chain methods:** `distinct()`, `group_by(*cols)`, `select_token(*cols)`, `cast(column, cql_type)`, `is_not_null(column)`, `is_null(column)`\n- **Terminal methods:** `sum(col)`, `avg(col)`, `min(col)`, `max(col)`, `aggregate(**funcs)`\n\n### Usage\n\n```python\n# TRUNCATE\nawait Product.truncate()\n\n# SELECT DISTINCT\npartitions = await Product.find().distinct().only(\"brand\").all()\n\n# GROUP BY + aggregates\nawait SensorReading.find().group_by(\"day\").all()\ntotal = await Product.find(brand=\"Acme\").sum(\"price\")\nstats = await Product.find().aggregate(total=\"sum(price)\", avg=\"avg(price)\")\n\n# IS NOT NULL / IS NULL (composable chain methods)\nawait Product.find().is_not_null(\"name\").all()\nawait Product.find().is_null(\"description\").all()\n\n# CAST in SELECT\nawait Product.find().cast(\"price\", \"int\").all()\n\n# TOKEN in SELECT projection\nawait Product.find().select_token(\"id\").all()\n```\n\n68 new unit tests (parametrized sync/async). All 984 tests pass.\n\nPlan: docs/plans/cql-gap-analysis.md\nPhase: 1\n\n<!-- START COPILOT CODING AGENT TIPS -->\n---\n\n✨ Let Copilot coding agent [set things up for you](https://github.com/fruch/coodie/issues/new?title=✨+Set+up+Copilot+instructions&body=Configure%20instructions%20for%20this%20repository%20as%20documented%20in%20%5BBest%20practices%20for%20Copilot%20coding%20agent%20in%20your%20repository%5D%28https://gh.io/copilot-coding-agent-tips%29%2E%0A%0A%3COnboard%20this%20repo%3E&assignees=copilot) — coding agent works faster and does higher quality work when set up for your repo.",
          "timestamp": "2026-03-08T00:08:29+02:00",
          "tree_id": "7572127fe32b95a1c0467b581d42b0cfb8f1826f",
          "url": "https://github.com/fruch/coodie/commit/b07f1cd6f693478a9e460e61ed7e4551d0eb4588"
        },
        "date": 1772921342760,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 54141.11569355992,
            "unit": "iter/sec",
            "range": "stddev: 0.000001951713959824159",
            "extra": "mean: 18.470251068707654 usec\nrounds: 8886"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_instantiation",
            "value": 1703303.8929708637,
            "unit": "iter/sec",
            "range": "stddev: 2.676894505012549e-7",
            "extra": "mean: 587.0942960482658 nsec\nrounds: 179212"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_serialization",
            "value": 153839.99203403186,
            "unit": "iter/sec",
            "range": "stddev: 0.000006673382319911644",
            "extra": "mean: 6.500260346989514 usec\nrounds: 21310"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 582581.3152695018,
            "unit": "iter/sec",
            "range": "stddev: 4.497304411274296e-7",
            "extra": "mean: 1.7164985793226146 usec\nrounds: 48570"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 612118.7732923733,
            "unit": "iter/sec",
            "range": "stddev: 3.6782139898560834e-7",
            "extra": "mean: 1.6336698752455325 usec\nrounds: 59838"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 808362.6436293889,
            "unit": "iter/sec",
            "range": "stddev: 3.4123702096416955e-7",
            "extra": "mean: 1.2370685457583706 usec\nrounds: 155473"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 848297.4100905119,
            "unit": "iter/sec",
            "range": "stddev: 3.4478363463590786e-7",
            "extra": "mean: 1.1788318437672722 usec\nrounds: 86491"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 705321.9040158151,
            "unit": "iter/sec",
            "range": "stddev: 3.690069592755525e-7",
            "extra": "mean: 1.4177923502820597 usec\nrounds: 106304"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 185177.79925505773,
            "unit": "iter/sec",
            "range": "stddev: 8.142700919329091e-7",
            "extra": "mean: 5.40021538231283 usec\nrounds: 7814"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "340979+fruch@users.noreply.github.com",
            "name": "fruch",
            "username": "fruch"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "b15b9f2320d1ed9d44823cd13ac419fb02702a72",
          "message": "test(integration): add LWT integration tests per §1.5 of cqlengine coverage plan\n\nUpdated the test coverage plan document and added extensive integration tests for conditional updates, deletes, and QuerySet operations to improve validation and reliability of the codebase.",
          "timestamp": "2026-03-08T00:09:01+02:00",
          "tree_id": "b88b349dc5f36c7cfc0b33ed96f7334eae8efe62",
          "url": "https://github.com/fruch/coodie/commit/b15b9f2320d1ed9d44823cd13ac419fb02702a72"
        },
        "date": 1772921385989,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 53740.18180309014,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015170435517726374",
            "extra": "mean: 18.60805018606205 usec\nrounds: 8090"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_instantiation",
            "value": 1704631.3449666968,
            "unit": "iter/sec",
            "range": "stddev: 2.2833577934696056e-7",
            "extra": "mean: 586.6371065818556 nsec\nrounds: 173883"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_serialization",
            "value": 155853.47645546508,
            "unit": "iter/sec",
            "range": "stddev: 0.000007247829324961025",
            "extra": "mean: 6.416282926391755 usec\nrounds: 19931"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 572401.637074467,
            "unit": "iter/sec",
            "range": "stddev: 4.447091672100892e-7",
            "extra": "mean: 1.747025052393245 usec\nrounds: 43229"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 614099.636296416,
            "unit": "iter/sec",
            "range": "stddev: 3.872543983648057e-7",
            "extra": "mean: 1.6284002479319433 usec\nrounds: 58956"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 834744.7960817856,
            "unit": "iter/sec",
            "range": "stddev: 3.3151409828889273e-7",
            "extra": "mean: 1.1979709303896315 usec\nrounds: 150535"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 843327.4618157556,
            "unit": "iter/sec",
            "range": "stddev: 3.437294167527125e-7",
            "extra": "mean: 1.1857790067062624 usec\nrounds: 97003"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 736995.5004383906,
            "unit": "iter/sec",
            "range": "stddev: 3.441372936428524e-7",
            "extra": "mean: 1.3568603870785714 usec\nrounds: 110792"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 185881.6471603019,
            "unit": "iter/sec",
            "range": "stddev: 8.897918751017688e-7",
            "extra": "mean: 5.379767262002004 usec\nrounds: 7777"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "91c05cb6fd9901401a7f39e731c423f3afe5691d",
          "message": "fix(ci): clarify relationship between MAX_CONTENT_LENGTH and CHUNK_THRESHOLD constants\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-09T02:13:22+02:00",
          "tree_id": "c6fe2b9b1a75bf15ef40332826d4b25afc1f93cc",
          "url": "https://github.com/fruch/coodie/commit/91c05cb6fd9901401a7f39e731c423f3afe5691d"
        },
        "date": 1773015251504,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 53365.87193148531,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015834686233509498",
            "extra": "mean: 18.73856762396513 usec\nrounds: 8148"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_instantiation",
            "value": 1758250.4545945306,
            "unit": "iter/sec",
            "range": "stddev: 2.1358827325826673e-7",
            "extra": "mean: 568.7471869476124 nsec\nrounds: 168322"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_serialization",
            "value": 155512.60743676202,
            "unit": "iter/sec",
            "range": "stddev: 0.000007892958760976772",
            "extra": "mean: 6.430346815493029 usec\nrounds: 18543"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 577183.3375453858,
            "unit": "iter/sec",
            "range": "stddev: 4.4506334874550367e-7",
            "extra": "mean: 1.732551747340362 usec\nrounds: 41606"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 597265.5141684565,
            "unit": "iter/sec",
            "range": "stddev: 4.0272081696052164e-7",
            "extra": "mean: 1.6742972367863076 usec\nrounds: 52258"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 809122.9209336174,
            "unit": "iter/sec",
            "range": "stddev: 3.3904864859333104e-7",
            "extra": "mean: 1.2359061573068977 usec\nrounds: 145307"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 822186.666779877,
            "unit": "iter/sec",
            "range": "stddev: 4.6652295413876924e-7",
            "extra": "mean: 1.2162688114568132 usec\nrounds: 29902"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 702920.6002380255,
            "unit": "iter/sec",
            "range": "stddev: 3.5302848733345686e-7",
            "extra": "mean: 1.4226357851247726 usec\nrounds: 126343"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 184072.1603776322,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010000309120597356",
            "extra": "mean: 5.432652053132075 usec\nrounds: 6478"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "29139614+renovate[bot]@users.noreply.github.com",
            "name": "renovate[bot]",
            "username": "renovate[bot]"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "05755ecd02e0512685493faf2cc90630620e163f",
          "message": "chore(deps): update github artifact actions",
          "timestamp": "2026-03-10T18:32:04+02:00",
          "tree_id": "7c2fcd6db8acf04b47703220de5acd34a478de96",
          "url": "https://github.com/fruch/coodie/commit/05755ecd02e0512685493faf2cc90630620e163f"
        },
        "date": 1773160363339,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 53627.63152276619,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014964810205203463",
            "extra": "mean: 18.647103584566782 usec\nrounds: 6835"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_instantiation",
            "value": 1701716.543272655,
            "unit": "iter/sec",
            "range": "stddev: 2.5609596621757275e-7",
            "extra": "mean: 587.6419336423977 nsec\nrounds: 169463"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_serialization",
            "value": 155644.6953068473,
            "unit": "iter/sec",
            "range": "stddev: 0.000009256817480505613",
            "extra": "mean: 6.424889701692306 usec\nrounds: 13808"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 557301.3702129371,
            "unit": "iter/sec",
            "range": "stddev: 4.7454527546983767e-7",
            "extra": "mean: 1.7943612799981346 usec\nrounds: 39313"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 616550.6300216034,
            "unit": "iter/sec",
            "range": "stddev: 4.5540690634641914e-7",
            "extra": "mean: 1.6219268155884632 usec\nrounds: 37426"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 840693.4283223149,
            "unit": "iter/sec",
            "range": "stddev: 3.4852312589178546e-7",
            "extra": "mean: 1.1894942511869004 usec\nrounds: 137855"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 817820.3719685104,
            "unit": "iter/sec",
            "range": "stddev: 3.35598137332301e-7",
            "extra": "mean: 1.2227623990253258 usec\nrounds: 69945"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 718648.8061301429,
            "unit": "iter/sec",
            "range": "stddev: 5.531264384546215e-7",
            "extra": "mean: 1.3915002591946226 usec\nrounds: 79089"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 188535.25369283266,
            "unit": "iter/sec",
            "range": "stddev: 7.293618261658131e-7",
            "extra": "mean: 5.3040478128787 usec\nrounds: 7864"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "29139614+renovate[bot]@users.noreply.github.com",
            "name": "renovate[bot]",
            "username": "renovate[bot]"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "0e924096538bf2fedef72cd4a90c0e666ee92968",
          "message": "chore(deps): lock file maintenance",
          "timestamp": "2026-03-10T18:32:59+02:00",
          "tree_id": "856b0c5215608735e721f2ff47b6e8f1bca2e4ba",
          "url": "https://github.com/fruch/coodie/commit/0e924096538bf2fedef72cd4a90c0e666ee92968"
        },
        "date": 1773160429114,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 78753.76026605561,
            "unit": "iter/sec",
            "range": "stddev: 7.83089334200476e-7",
            "extra": "mean: 12.697806385646567 usec\nrounds: 8801"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_instantiation",
            "value": 1714463.8671099972,
            "unit": "iter/sec",
            "range": "stddev: 2.1364059220334252e-7",
            "extra": "mean: 583.2727181854581 nsec\nrounds: 160026"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_serialization",
            "value": 161571.58989920493,
            "unit": "iter/sec",
            "range": "stddev: 0.000008734400637015216",
            "extra": "mean: 6.189206905891324 usec\nrounds: 18448"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 561144.9188207142,
            "unit": "iter/sec",
            "range": "stddev: 3.63621564771413e-7",
            "extra": "mean: 1.7820708456232142 usec\nrounds: 44110"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 643757.3785835037,
            "unit": "iter/sec",
            "range": "stddev: 2.4632915012606587e-7",
            "extra": "mean: 1.5533802535985801 usec\nrounds: 43137"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 864763.689223022,
            "unit": "iter/sec",
            "range": "stddev: 3.7492579625067414e-7",
            "extra": "mean: 1.156385278963882 usec\nrounds: 112791"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 819227.7477712072,
            "unit": "iter/sec",
            "range": "stddev: 2.2788499581135562e-7",
            "extra": "mean: 1.2206617789993102 usec\nrounds: 73041"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 787911.0229684659,
            "unit": "iter/sec",
            "range": "stddev: 2.3633040722263808e-7",
            "extra": "mean: 1.269178842342484 usec\nrounds: 92014"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 187208.54704661743,
            "unit": "iter/sec",
            "range": "stddev: 4.1620322590977096e-7",
            "extra": "mean: 5.341636457180487 usec\nrounds: 7779"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "4e836748c6d6e3664bb1f30e9625bc42d0550543",
          "message": "\"Claude Code Review workflow\"",
          "timestamp": "2026-03-10T23:35:19+02:00",
          "tree_id": "f87d9b638fe1f0efdec33214f99d7d616f553ef3",
          "url": "https://github.com/fruch/coodie/commit/4e836748c6d6e3664bb1f30e9625bc42d0550543"
        },
        "date": 1773178602048,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 52518.78708187321,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020854591131570416",
            "extra": "mean: 19.040805311079787 usec\nrounds: 7833"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_instantiation",
            "value": 1637781.5263259148,
            "unit": "iter/sec",
            "range": "stddev: 3.092716309667793e-7",
            "extra": "mean: 610.5820489032689 nsec\nrounds: 182117"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_serialization",
            "value": 153912.81629380147,
            "unit": "iter/sec",
            "range": "stddev: 0.000008430318049605875",
            "extra": "mean: 6.497184731459384 usec\nrounds: 16570"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 571355.0842602829,
            "unit": "iter/sec",
            "range": "stddev: 4.6790078330157987e-7",
            "extra": "mean: 1.7502250833991813 usec\nrounds: 44659"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 616832.7805345483,
            "unit": "iter/sec",
            "range": "stddev: 3.925808754358872e-7",
            "extra": "mean: 1.6211849168155401 usec\nrounds: 43625"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 834335.5295838552,
            "unit": "iter/sec",
            "range": "stddev: 3.2350616369064655e-7",
            "extra": "mean: 1.1985585709130402 usec\nrounds: 150083"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 796447.6986219032,
            "unit": "iter/sec",
            "range": "stddev: 3.5479279896832e-7",
            "extra": "mean: 1.2555752270115215 usec\nrounds: 80822"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 743147.891671363,
            "unit": "iter/sec",
            "range": "stddev: 3.230832971706621e-7",
            "extra": "mean: 1.3456271775877189 usec\nrounds: 87712"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 179684.13596350548,
            "unit": "iter/sec",
            "range": "stddev: 7.265297814212797e-7",
            "extra": "mean: 5.565321582997754 usec\nrounds: 7631"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "fruch@scylladb.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "8e27db80d5e8fd158aef7f58bbf282e52a45a4aa",
          "message": "docs(plans): add Phase 10 performance improvement plan with 9 targeted optimizations\n\nCo-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>",
          "timestamp": "2026-03-11T01:02:46+02:00",
          "tree_id": "88b5fcd9e423f5b004a4eba27fdffdf583ad9c8f",
          "url": "https://github.com/fruch/coodie/commit/8e27db80d5e8fd158aef7f58bbf282e52a45a4aa"
        },
        "date": 1773183804647,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 53419.55937128613,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016617542107921262",
            "extra": "mean: 18.719735088970353 usec\nrounds: 7025"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_instantiation",
            "value": 1693135.617368042,
            "unit": "iter/sec",
            "range": "stddev: 3.7756420234062286e-7",
            "extra": "mean: 590.6201427352213 nsec\nrounds: 182150"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_serialization",
            "value": 151094.9667709403,
            "unit": "iter/sec",
            "range": "stddev: 0.000008286372452028547",
            "extra": "mean: 6.618354147534235 usec\nrounds: 18529"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 571197.2625461939,
            "unit": "iter/sec",
            "range": "stddev: 4.0283574897703647e-7",
            "extra": "mean: 1.7507086703153238 usec\nrounds: 39814"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 611404.2357970023,
            "unit": "iter/sec",
            "range": "stddev: 4.148480162390017e-7",
            "extra": "mean: 1.6355791168120377 usec\nrounds: 45041"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 845745.1678159372,
            "unit": "iter/sec",
            "range": "stddev: 3.469128791627076e-7",
            "extra": "mean: 1.182389256308035 usec\nrounds: 139412"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 800216.0434448923,
            "unit": "iter/sec",
            "range": "stddev: 3.4907429372714665e-7",
            "extra": "mean: 1.2496625232544043 usec\nrounds: 73611"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 736774.1872221694,
            "unit": "iter/sec",
            "range": "stddev: 3.186005618469826e-7",
            "extra": "mean: 1.357267962617231 usec\nrounds: 89199"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 188150.5002667756,
            "unit": "iter/sec",
            "range": "stddev: 9.083806382267908e-7",
            "extra": "mean: 5.314894186207933 usec\nrounds: 7551"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "29139614+renovate[bot]@users.noreply.github.com",
            "name": "renovate[bot]",
            "username": "renovate[bot]"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "cc8732384208ae5ce9aab56adb887f42f1a71c13",
          "message": "chore(deps): update actions/checkout action to v6",
          "timestamp": "2026-03-16T08:25:10+02:00",
          "tree_id": "03f0b427b1ac74a28f7cabbf013cb1daf8ff5e79",
          "url": "https://github.com/fruch/coodie/commit/cc8732384208ae5ce9aab56adb887f42f1a71c13"
        },
        "date": 1773642346729,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 52422.38414897164,
            "unit": "iter/sec",
            "range": "stddev: 0.000001935427090746144",
            "extra": "mean: 19.07582068679371 usec\nrounds: 7802"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_instantiation",
            "value": 1605382.181718204,
            "unit": "iter/sec",
            "range": "stddev: 3.367466432451592e-7",
            "extra": "mean: 622.9046337923862 nsec\nrounds: 162049"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_serialization",
            "value": 153976.0819915541,
            "unit": "iter/sec",
            "range": "stddev: 0.000008746271991363469",
            "extra": "mean: 6.49451516797818 usec\nrounds: 18427"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 563257.6602481196,
            "unit": "iter/sec",
            "range": "stddev: 4.936648799093072e-7",
            "extra": "mean: 1.7753864182858905 usec\nrounds: 41556"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 600794.0497229896,
            "unit": "iter/sec",
            "range": "stddev: 5.571758648035074e-7",
            "extra": "mean: 1.6644638881844351 usec\nrounds: 44459"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 840010.3786910819,
            "unit": "iter/sec",
            "range": "stddev: 3.618817518213359e-7",
            "extra": "mean: 1.1904614816286159 usec\nrounds: 111025"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 843873.6444565101,
            "unit": "iter/sec",
            "range": "stddev: 3.6859264128900245e-7",
            "extra": "mean: 1.185011531725276 usec\nrounds: 61309"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 736429.2883813075,
            "unit": "iter/sec",
            "range": "stddev: 3.7905514115428463e-7",
            "extra": "mean: 1.3579036246616811 usec\nrounds: 75621"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 180585.91260882127,
            "unit": "iter/sec",
            "range": "stddev: 7.538864945752134e-7",
            "extra": "mean: 5.537530505860466 usec\nrounds: 7097"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "29139614+renovate[bot]@users.noreply.github.com",
            "name": "renovate[bot]",
            "username": "renovate[bot]"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "d037614026b4e77b3385905b147f338d2591de53",
          "message": "chore(deps): update pre-commit hook astral-sh/ruff-pre-commit to v0.15.5",
          "timestamp": "2026-03-16T08:25:46+02:00",
          "tree_id": "a45ac94eed2ac872935576690d19717e3186cbef",
          "url": "https://github.com/fruch/coodie/commit/d037614026b4e77b3385905b147f338d2591de53"
        },
        "date": 1773642432646,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 53254.93049478449,
            "unit": "iter/sec",
            "range": "stddev: 0.00000207776846212492",
            "extra": "mean: 18.777604077390258 usec\nrounds: 8633"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_instantiation",
            "value": 1714853.699689593,
            "unit": "iter/sec",
            "range": "stddev: 2.2497143056322292e-7",
            "extra": "mean: 583.1401245371607 nsec\nrounds: 180832"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_serialization",
            "value": 158202.59505834724,
            "unit": "iter/sec",
            "range": "stddev: 0.000008649676327382556",
            "extra": "mean: 6.321008828149668 usec\nrounds: 14952"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 572269.5964444677,
            "unit": "iter/sec",
            "range": "stddev: 5.623904085858073e-7",
            "extra": "mean: 1.747428146127345 usec\nrounds: 45001"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 603090.6127481044,
            "unit": "iter/sec",
            "range": "stddev: 4.3646135206944237e-7",
            "extra": "mean: 1.6581256263354816 usec\nrounds: 47896"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 853500.4692086627,
            "unit": "iter/sec",
            "range": "stddev: 3.083952495643582e-7",
            "extra": "mean: 1.171645518750759 usec\nrounds: 149187"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 843053.4251512617,
            "unit": "iter/sec",
            "range": "stddev: 5.548280000421511e-7",
            "extra": "mean: 1.1861644471945283 usec\nrounds: 76371"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 742391.8098213815,
            "unit": "iter/sec",
            "range": "stddev: 3.437239266208038e-7",
            "extra": "mean: 1.3469976187380066 usec\nrounds: 71809"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 181101.72762592562,
            "unit": "iter/sec",
            "range": "stddev: 7.808748222695238e-7",
            "extra": "mean: 5.521758478558241 usec\nrounds: 7991"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "29139614+renovate[bot]@users.noreply.github.com",
            "name": "renovate[bot]",
            "username": "renovate[bot]"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "14e3341a04d552fc9d3db87063a7bf42ef1634e4",
          "message": "chore(deps): lock file maintenance",
          "timestamp": "2026-03-19T17:35:51+02:00",
          "tree_id": "f2271980f65bf6056df021ad4f29f433b101aa34",
          "url": "https://github.com/fruch/coodie/commit/14e3341a04d552fc9d3db87063a7bf42ef1634e4"
        },
        "date": 1773934589328,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 45210.4745147853,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013948244469244525",
            "extra": "mean: 22.118768067186892 usec\nrounds: 7140"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_instantiation",
            "value": 1749467.462364434,
            "unit": "iter/sec",
            "range": "stddev: 3.375708239354202e-7",
            "extra": "mean: 571.6025142007977 nsec\nrounds: 153847"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_serialization",
            "value": 141117.51004046254,
            "unit": "iter/sec",
            "range": "stddev: 0.00003393788060188194",
            "extra": "mean: 7.086292832925345 usec\nrounds: 16757"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 515731.01577574736,
            "unit": "iter/sec",
            "range": "stddev: 6.22744469970092e-7",
            "extra": "mean: 1.9389952696481314 usec\nrounds: 40166"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 589787.4797703486,
            "unit": "iter/sec",
            "range": "stddev: 4.1689367130485213e-7",
            "extra": "mean: 1.6955259891060757 usec\nrounds: 40440"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 780761.4236189531,
            "unit": "iter/sec",
            "range": "stddev: 5.11722111389811e-7",
            "extra": "mean: 1.2808009844605812 usec\nrounds: 99751"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 814219.2672896283,
            "unit": "iter/sec",
            "range": "stddev: 4.767139081473803e-7",
            "extra": "mean: 1.2281703960762294 usec\nrounds: 68018"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 668002.1941661546,
            "unit": "iter/sec",
            "range": "stddev: 5.113211825013381e-7",
            "extra": "mean: 1.4970010708546662 usec\nrounds: 82177"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 179389.17211991496,
            "unit": "iter/sec",
            "range": "stddev: 7.944464265125644e-7",
            "extra": "mean: 5.57447246220378 usec\nrounds: 7408"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "b687365765a07f2d516551cebfd0cb3c13eb2495",
          "message": "fix(types): restore ISNULL value in cache key for correct IS NULL / IS NOT NULL distinction\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-03-19T17:45:14+02:00",
          "tree_id": "f9161a6d05dba4c9e13fd57db79af78e4302ceb0",
          "url": "https://github.com/fruch/coodie/commit/b687365765a07f2d516551cebfd0cb3c13eb2495"
        },
        "date": 1773935213815,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 52888.76543123329,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016412812864983776",
            "extra": "mean: 18.907607160923693 usec\nrounds: 7848"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_instantiation",
            "value": 1708290.7282181263,
            "unit": "iter/sec",
            "range": "stddev: 2.1661518606455754e-7",
            "extra": "mean: 585.380452800955 nsec\nrounds: 181489"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_serialization",
            "value": 147128.66459197312,
            "unit": "iter/sec",
            "range": "stddev: 0.00003008119840377938",
            "extra": "mean: 6.796772082267352 usec\nrounds: 19314"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 569052.7613801511,
            "unit": "iter/sec",
            "range": "stddev: 4.59544550528751e-7",
            "extra": "mean: 1.7573062954209233 usec\nrounds: 43778"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 613746.4835471258,
            "unit": "iter/sec",
            "range": "stddev: 4.6946549064029214e-7",
            "extra": "mean: 1.629337237454357 usec\nrounds: 46190"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 811952.631821649,
            "unit": "iter/sec",
            "range": "stddev: 3.8848081607266695e-7",
            "extra": "mean: 1.2315989391603535 usec\nrounds: 151012"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 845974.2367164021,
            "unit": "iter/sec",
            "range": "stddev: 3.559571680434635e-7",
            "extra": "mean: 1.1820690945405614 usec\nrounds: 75621"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 721944.4219012149,
            "unit": "iter/sec",
            "range": "stddev: 3.620970479357629e-7",
            "extra": "mean: 1.3851481771498917 usec\nrounds: 90736"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 182901.92064445108,
            "unit": "iter/sec",
            "range": "stddev: 8.601814102640509e-7",
            "extra": "mean: 5.467411148426003 usec\nrounds: 6871"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "29139614+renovate[bot]@users.noreply.github.com",
            "name": "renovate[bot]",
            "username": "renovate[bot]"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "7902c326d74ecdf0454e520dda1decc329e6ed0c",
          "message": "chore(deps): update pre-commit hook astral-sh/ruff-pre-commit to v0.15.6",
          "timestamp": "2026-03-23T06:40:56+02:00",
          "tree_id": "92c23f4e2afae4160b1b7579ada7cb854e45f45c",
          "url": "https://github.com/fruch/coodie/commit/7902c326d74ecdf0454e520dda1decc329e6ed0c"
        },
        "date": 1774240892338,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 53174.081551664654,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017183370590345018",
            "extra": "mean: 18.80615463058608 usec\nrounds: 8433"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_instantiation",
            "value": 1642250.854891053,
            "unit": "iter/sec",
            "range": "stddev: 3.2266775586367267e-7",
            "extra": "mean: 608.9203711002727 nsec\nrounds: 193799"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_serialization",
            "value": 149971.2258913593,
            "unit": "iter/sec",
            "range": "stddev: 0.00002658836423985084",
            "extra": "mean: 6.667945761304974 usec\nrounds: 19322"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 576647.4263356354,
            "unit": "iter/sec",
            "range": "stddev: 4.110405693726568e-7",
            "extra": "mean: 1.7341619060967666 usec\nrounds: 43587"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 616374.0223521875,
            "unit": "iter/sec",
            "range": "stddev: 4.0140152543700426e-7",
            "extra": "mean: 1.6223915410708434 usec\nrounds: 37286"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 837357.9909437413,
            "unit": "iter/sec",
            "range": "stddev: 3.7872685533504344e-7",
            "extra": "mean: 1.1942323484283628 usec\nrounds: 145497"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 882691.0450756117,
            "unit": "iter/sec",
            "range": "stddev: 3.1727983933411134e-7",
            "extra": "mean: 1.1328992240023683 usec\nrounds: 78223"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 659836.2107527644,
            "unit": "iter/sec",
            "range": "stddev: 3.5965585858270873e-7",
            "extra": "mean: 1.5155276168598943 usec\nrounds: 91828"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 182987.3729048551,
            "unit": "iter/sec",
            "range": "stddev: 8.148552437787919e-7",
            "extra": "mean: 5.464857952356929 usec\nrounds: 7765"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "fruch@scylladb.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "c638b9307b6c795582c8187bea0f6ad3c5a583a5",
          "message": "chore: update repo links from fruch to scylladb org\n\nThe repository has moved from fruch/coodie to scylladb/coodie.\nUpdate all GitHub URLs, GitHub Pages links, and org references\nacross documentation, configuration, and workflow files.\n\nCo-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-14T12:58:49+03:00",
          "tree_id": "1e9fe1a2bf21a3a667ac58946d1a456fde051453",
          "url": "https://github.com/scylladb/coodie/commit/c638b9307b6c795582c8187bea0f6ad3c5a583a5"
        },
        "date": 1776160762780,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 54995.64416847388,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015604995648491813",
            "extra": "mean: 18.18325824017255 usec\nrounds: 6978"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_instantiation",
            "value": 1603229.767273206,
            "unit": "iter/sec",
            "range": "stddev: 2.3067588064024034e-7",
            "extra": "mean: 623.7409137561192 nsec\nrounds: 152208"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_serialization",
            "value": 148376.7676965524,
            "unit": "iter/sec",
            "range": "stddev: 0.000007533070274477889",
            "extra": "mean: 6.7395995715792605 usec\nrounds: 14472"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 546152.9244666528,
            "unit": "iter/sec",
            "range": "stddev: 4.69955877682855e-7",
            "extra": "mean: 1.830989005463173 usec\nrounds: 39656"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 589286.7593556659,
            "unit": "iter/sec",
            "range": "stddev: 4.2137214399055486e-7",
            "extra": "mean: 1.6969666874806648 usec\nrounds: 41606"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 812866.9303701958,
            "unit": "iter/sec",
            "range": "stddev: 3.438612217456525e-7",
            "extra": "mean: 1.2302136581501477 usec\nrounds: 145349"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 825500.4198041646,
            "unit": "iter/sec",
            "range": "stddev: 4.222433626704501e-7",
            "extra": "mean: 1.211386422113792 usec\nrounds: 64885"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 621847.416479851,
            "unit": "iter/sec",
            "range": "stddev: 4.240342507169435e-7",
            "extra": "mean: 1.6081115294500894 usec\nrounds: 79943"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 178575.83206069114,
            "unit": "iter/sec",
            "range": "stddev: 8.72032545046559e-7",
            "extra": "mean: 5.599861909981962 usec\nrounds: 7372"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "b3f831c5381e24eecbc57450d6d2eddb0250512a",
          "message": "style: fix ruff format for _SLASH_COMMAND_WORKFLOWS list comprehension\n\nAgent-Logs-Url: https://github.com/scylladb/coodie/sessions/c1fc1aa4-7772-4d89-9b36-be51e8946cfb\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-04-14T13:34:10+03:00",
          "tree_id": "78f53180a9fed0e8085c44f57ae2272c89c371b2",
          "url": "https://github.com/scylladb/coodie/commit/b3f831c5381e24eecbc57450d6d2eddb0250512a"
        },
        "date": 1776162886177,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 54883.12272921444,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015389992781659601",
            "extra": "mean: 18.220537576439636 usec\nrounds: 6866"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_instantiation",
            "value": 1627134.4006353011,
            "unit": "iter/sec",
            "range": "stddev: 2.4723275139888465e-7",
            "extra": "mean: 614.5773819357258 nsec\nrounds: 148368"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_serialization",
            "value": 149004.63954110138,
            "unit": "iter/sec",
            "range": "stddev: 0.000007210071063241413",
            "extra": "mean: 6.711200423555673 usec\nrounds: 16999"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 531289.4593719585,
            "unit": "iter/sec",
            "range": "stddev: 5.265729015743675e-7",
            "extra": "mean: 1.8822131370385327 usec\nrounds: 41227"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 570406.25593908,
            "unit": "iter/sec",
            "range": "stddev: 4.280020403482602e-7",
            "extra": "mean: 1.7531364524634543 usec\nrounds: 41956"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 811480.635505154,
            "unit": "iter/sec",
            "range": "stddev: 3.6841394671411434e-7",
            "extra": "mean: 1.2323152965658768 usec\nrounds: 119589"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 825720.2103670368,
            "unit": "iter/sec",
            "range": "stddev: 3.8427091557352614e-7",
            "extra": "mean: 1.211063974751805 usec\nrounds: 65604"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 603869.3868010868,
            "unit": "iter/sec",
            "range": "stddev: 4.3922843503494703e-7",
            "extra": "mean: 1.6559872413757544 usec\nrounds: 82454"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 177343.55210167987,
            "unit": "iter/sec",
            "range": "stddev: 8.64074199215768e-7",
            "extra": "mean: 5.638772812144026 usec\nrounds: 7496"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "fruch@scylladb.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "eee85f7e29040ad57da38623f47c7e97879ccc2b",
          "message": "fix(ci): set up automatic releases with PyPI Trusted Publishing\n\nThe release pipeline was non-functional: ci.yml targeted branch `main`\nbut the default branch is `master`, so the release job never fired.\n\n- Fix branch references from `main` to `master` in ci.yml and pyproject.toml\n- Update semantic-release config to v10 branches format\n- Split monolithic release job into release/build/publish-to-pypi jobs\n- Use Trusted Publishing (OIDC) for PyPI — no API token needed\n- Delete redundant publish.yml (GITHUB_TOKEN tags don't trigger workflows)\n- Update CONTRIBUTING.md release documentation\n\nCo-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-14T13:36:49+03:00",
          "tree_id": "c712f6d56df7f93ca2e9bd9c739c6efde0ae51c3",
          "url": "https://github.com/scylladb/coodie/commit/eee85f7e29040ad57da38623f47c7e97879ccc2b"
        },
        "date": 1776163047898,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 78237.80362789263,
            "unit": "iter/sec",
            "range": "stddev: 8.28714021369749e-7",
            "extra": "mean: 12.781544900673683 usec\nrounds: 8207"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_instantiation",
            "value": 1760419.28126437,
            "unit": "iter/sec",
            "range": "stddev: 1.6867346784750116e-7",
            "extra": "mean: 568.0464936067838 nsec\nrounds: 150967"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_serialization",
            "value": 161356.47501334673,
            "unit": "iter/sec",
            "range": "stddev: 0.000009829026874059864",
            "extra": "mean: 6.197458143017093 usec\nrounds: 19053"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 563525.2443793446,
            "unit": "iter/sec",
            "range": "stddev: 3.202460938923607e-7",
            "extra": "mean: 1.7745433944159499 usec\nrounds: 46158"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 630633.2506238408,
            "unit": "iter/sec",
            "range": "stddev: 2.774409892478413e-7",
            "extra": "mean: 1.5857076977954632 usec\nrounds: 47793"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 873590.6388377642,
            "unit": "iter/sec",
            "range": "stddev: 2.356971512903625e-7",
            "extra": "mean: 1.1447009108641693 usec\nrounds: 99355"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 840623.3035051861,
            "unit": "iter/sec",
            "range": "stddev: 2.6292206266801967e-7",
            "extra": "mean: 1.1895934788272624 usec\nrounds: 72380"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 689540.043854628,
            "unit": "iter/sec",
            "range": "stddev: 2.9208534442691394e-7",
            "extra": "mean: 1.4502420982106512 usec\nrounds: 91467"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 189107.08183888535,
            "unit": "iter/sec",
            "range": "stddev: 5.422455275341539e-7",
            "extra": "mean: 5.28800926055205 usec\nrounds: 7343"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "fruch@scylladb.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "ca54eca21e2bac1ad4e5625b8503a86add559ed6",
          "message": "fix(ci): grant pull-requests write permission to claude-code-review workflow\n\nThe Claude Code Action needs write access to post review comments on PRs.\nWith only read permission, the OIDC token exchange fails with 401 Unauthorized.\n\nCo-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-14T13:37:20+03:00",
          "tree_id": "c6986dfa517d4f4e8ab1cf9decef5edaf3455118",
          "url": "https://github.com/scylladb/coodie/commit/ca54eca21e2bac1ad4e5625b8503a86add559ed6"
        },
        "date": 1776163101559,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 63510.94758389892,
            "unit": "iter/sec",
            "range": "stddev: 0.000001832860274462848",
            "extra": "mean: 15.745316957820304 usec\nrounds: 8244"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_instantiation",
            "value": 2560342.083205457,
            "unit": "iter/sec",
            "range": "stddev: 5.567404116165053e-8",
            "extra": "mean: 390.5728092193195 nsec\nrounds: 116374"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_serialization",
            "value": 191084.1997152525,
            "unit": "iter/sec",
            "range": "stddev: 0.000004485218071659442",
            "extra": "mean: 5.233295068300611 usec\nrounds: 20419"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 662269.4181515708,
            "unit": "iter/sec",
            "range": "stddev: 3.7139971892127077e-7",
            "extra": "mean: 1.50995950075885 usec\nrounds: 47754"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 783639.1636904074,
            "unit": "iter/sec",
            "range": "stddev: 3.001420299522129e-7",
            "extra": "mean: 1.2760975284730287 usec\nrounds: 45761"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 1078393.0794420769,
            "unit": "iter/sec",
            "range": "stddev: 2.84008292795129e-7",
            "extra": "mean: 927.3056541844327 nsec\nrounds: 166973"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 1018018.8448498714,
            "unit": "iter/sec",
            "range": "stddev: 2.792873166512359e-7",
            "extra": "mean: 982.3000871339187 nsec\nrounds: 75758"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 804473.1343303258,
            "unit": "iter/sec",
            "range": "stddev: 3.285877124385723e-7",
            "extra": "mean: 1.2430495902544194 usec\nrounds: 92619"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 225964.88933983413,
            "unit": "iter/sec",
            "range": "stddev: 5.788978125061892e-7",
            "extra": "mean: 4.425466287800472 usec\nrounds: 7742"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "fruch@scylladb.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "262e2571f0961657758a3faa4497f9578c79ae37",
          "message": "docs: add PyPI downloads badge and fix branch references in README\n\n- Add monthly downloads badge from shields.io/pypi\n- Fix badge branch parameters from `main` to `master`\n- Fix LICENSE, CONTRIBUTING.md, CHANGELOG.md links to use `blob/master`\n\nCo-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-14T14:01:51+03:00",
          "tree_id": "4e0e37788eba91f23689e753022cfa29118dee8e",
          "url": "https://github.com/scylladb/coodie/commit/262e2571f0961657758a3faa4497f9578c79ae37"
        },
        "date": 1776164555155,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 63905.2680713563,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018099614484771073",
            "extra": "mean: 15.648162196634633 usec\nrounds: 8613"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_instantiation",
            "value": 1968950.7386573046,
            "unit": "iter/sec",
            "range": "stddev: 7.8942176114706e-8",
            "extra": "mean: 507.8847227442239 nsec\nrounds: 197278"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_serialization",
            "value": 147193.80767105654,
            "unit": "iter/sec",
            "range": "stddev: 0.00000838215742686631",
            "extra": "mean: 6.79376405721336 usec\nrounds: 18407"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 575675.5123501236,
            "unit": "iter/sec",
            "range": "stddev: 5.302429803371564e-7",
            "extra": "mean: 1.7370896947094805 usec\nrounds: 48810"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 630992.1389203371,
            "unit": "iter/sec",
            "range": "stddev: 4.287511012805092e-7",
            "extra": "mean: 1.584805797598455 usec\nrounds: 58645"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 855695.7444380457,
            "unit": "iter/sec",
            "range": "stddev: 3.646039817287494e-7",
            "extra": "mean: 1.1686396788810984 usec\nrounds: 168039"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 866186.7653543993,
            "unit": "iter/sec",
            "range": "stddev: 3.6998814122457345e-7",
            "extra": "mean: 1.1544854296992764 usec\nrounds: 83732"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 636206.5429816344,
            "unit": "iter/sec",
            "range": "stddev: 6.046119005195612e-7",
            "extra": "mean: 1.5718165916895754 usec\nrounds: 90901"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 182887.09097620545,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015052945545864369",
            "extra": "mean: 5.467854481485 usec\nrounds: 7676"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "fruch@scylladb.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "56e436d2e886005c1d1940e10b7cbe30d190affb",
          "message": "fix(demos): address review feedback and fix Starlette 1.0 / Chart.js compat\n\nCache sensor discovery, fix date pagination cursor, fix CI lint.\nUpdate TemplateResponse calls for Starlette 1.0 API (request, name, context).\nDestroy Chart.js instances before reinitializing to prevent canvas reuse errors.\n\nCo-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-14T16:20:41+03:00",
          "tree_id": "197293d9d2f64beeb1ec6c8aa5e94a87f9227b84",
          "url": "https://github.com/scylladb/coodie/commit/56e436d2e886005c1d1940e10b7cbe30d190affb"
        },
        "date": 1776172880928,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 63390.891274873095,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015535919947115685",
            "extra": "mean: 15.7751370881321 usec\nrounds: 12109"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_instantiation",
            "value": 1565172.084963614,
            "unit": "iter/sec",
            "range": "stddev: 2.691006071495736e-7",
            "extra": "mean: 638.9073825216142 nsec\nrounds: 194175"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_serialization",
            "value": 148693.48311746848,
            "unit": "iter/sec",
            "range": "stddev: 0.000007924622233107804",
            "extra": "mean: 6.725244301460043 usec\nrounds: 19742"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 572257.236510232,
            "unit": "iter/sec",
            "range": "stddev: 5.210710777839605e-7",
            "extra": "mean: 1.7474658880650433 usec\nrounds: 45893"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 633450.8981485803,
            "unit": "iter/sec",
            "range": "stddev: 5.004181075190432e-7",
            "extra": "mean: 1.5786543249409728 usec\nrounds: 59446"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 855331.0040868073,
            "unit": "iter/sec",
            "range": "stddev: 3.880412023687484e-7",
            "extra": "mean: 1.1691380240187228 usec\nrounds: 159465"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 857744.9297029709,
            "unit": "iter/sec",
            "range": "stddev: 3.9573796157596164e-7",
            "extra": "mean: 1.165847754234223 usec\nrounds: 107090"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 655470.5751686463,
            "unit": "iter/sec",
            "range": "stddev: 4.363098984110662e-7",
            "extra": "mean: 1.5256214968043524 usec\nrounds: 134699"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 182592.63998847705,
            "unit": "iter/sec",
            "range": "stddev: 9.794697570554902e-7",
            "extra": "mean: 5.47667200640238 usec\nrounds: 7491"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "fruch@scylladb.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "ea0bf210a556116d58433be1229dd7993fb42bd9",
          "message": "feat(demos): add realtime-counters demo with CounterDocument and traffic simulator\n\nDemonstrates Cassandra counter columns via coodie's CounterDocument:\n- Increment/decrement counters per page with atomic updates\n- Traffic simulator with configurable virtual users for realtime activity\n- HTMX dashboard with live counter updates and aggregate totals\n- Time-bucketed counters sorted by date descending\n\nCo-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-14T16:21:00+03:00",
          "tree_id": "e186c1332c53073f51bedec2fb923b38f289d17f",
          "url": "https://github.com/scylladb/coodie/commit/ea0bf210a556116d58433be1229dd7993fb42bd9"
        },
        "date": 1776172905930,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 64293.64250074137,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024502279815457933",
            "extra": "mean: 15.553637359844233 usec\nrounds: 8030"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_instantiation",
            "value": 1563471.905765964,
            "unit": "iter/sec",
            "range": "stddev: 2.5100947824319436e-7",
            "extra": "mean: 639.6021548657683 nsec\nrounds: 178572"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_serialization",
            "value": 148653.89484358186,
            "unit": "iter/sec",
            "range": "stddev: 0.000009597535644496827",
            "extra": "mean: 6.727035312813232 usec\nrounds: 16368"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 577460.5401016498,
            "unit": "iter/sec",
            "range": "stddev: 5.405229749635235e-7",
            "extra": "mean: 1.7317200580042595 usec\nrounds: 44127"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 604535.3718559874,
            "unit": "iter/sec",
            "range": "stddev: 4.850110094089382e-7",
            "extra": "mean: 1.6541629266950824 usec\nrounds: 45143"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 827114.7182455581,
            "unit": "iter/sec",
            "range": "stddev: 4.1217638747064597e-7",
            "extra": "mean: 1.2090221319252534 usec\nrounds: 147886"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 871353.2546701265,
            "unit": "iter/sec",
            "range": "stddev: 3.687795720065324e-7",
            "extra": "mean: 1.1476401730760462 usec\nrounds: 78346"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 633448.943316711,
            "unit": "iter/sec",
            "range": "stddev: 4.510709649346696e-7",
            "extra": "mean: 1.578659196689229 usec\nrounds: 92593"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 186070.6205285679,
            "unit": "iter/sec",
            "range": "stddev: 9.648287311136312e-7",
            "extra": "mean: 5.374303569039087 usec\nrounds: 7537"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "340979+fruch@users.noreply.github.com",
            "name": "fruch",
            "username": "fruch"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "c67deaf11bed8d6f8d3bc137359d61a3133f2e08",
          "message": "feat(demos): add collections-tags demo with interactive multi-tag cloud filtering\n\nA runnable demo app showcasing coodie's CQL collection types and mutation\noperations with an interactive tag cloud supporting multi-tag selection\nfor filtering articles.",
          "timestamp": "2026-04-14T16:21:24+03:00",
          "tree_id": "fb8d7fd83717b5c441a552174a5b05becbb995e4",
          "url": "https://github.com/scylladb/coodie/commit/c67deaf11bed8d6f8d3bc137359d61a3133f2e08"
        },
        "date": 1776172919704,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 77697.09747659553,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011051883020717053",
            "extra": "mean: 12.870493653913224 usec\nrounds: 8194"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_instantiation",
            "value": 1791024.8912103134,
            "unit": "iter/sec",
            "range": "stddev: 1.9023388904016705e-7",
            "extra": "mean: 558.3395322463855 nsec\nrounds: 143144"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_serialization",
            "value": 161559.71910176397,
            "unit": "iter/sec",
            "range": "stddev: 0.000009349435845478984",
            "extra": "mean: 6.18966166541869 usec\nrounds: 18662"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 577553.4432269495,
            "unit": "iter/sec",
            "range": "stddev: 2.9152227863761576e-7",
            "extra": "mean: 1.731441499877008 usec\nrounds: 45017"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 642366.5579206155,
            "unit": "iter/sec",
            "range": "stddev: 4.4038159763690424e-7",
            "extra": "mean: 1.5567435565716068 usec\nrounds: 34764"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 866495.7647040761,
            "unit": "iter/sec",
            "range": "stddev: 2.4320664612277857e-7",
            "extra": "mean: 1.1540737309218332 usec\nrounds: 89040"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 848185.5703870557,
            "unit": "iter/sec",
            "range": "stddev: 2.701542405161276e-7",
            "extra": "mean: 1.1789872816908051 usec\nrounds: 60857"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 683894.8241425923,
            "unit": "iter/sec",
            "range": "stddev: 3.399028946637937e-7",
            "extra": "mean: 1.4622131425745366 usec\nrounds: 83606"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 193081.6508966056,
            "unit": "iter/sec",
            "range": "stddev: 6.071848142942469e-7",
            "extra": "mean: 5.179156048005285 usec\nrounds: 7581"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "29139614+renovate[bot]@users.noreply.github.com",
            "name": "renovate[bot]",
            "username": "renovate[bot]"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "cdae2c262c6b311641acff7dde04f8ce5c9b733e",
          "message": "chore(deps): update pre-commit hooks (non-major)",
          "timestamp": "2026-04-14T16:44:47+03:00",
          "tree_id": "445ad0edea1ad7118bee94afeeb561e7f21c29d5",
          "url": "https://github.com/scylladb/coodie/commit/cdae2c262c6b311641acff7dde04f8ce5c9b733e"
        },
        "date": 1776174331431,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 61959.20672997299,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019961732835490046",
            "extra": "mean: 16.139651438052486 usec\nrounds: 7858"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_instantiation",
            "value": 1577739.6098099304,
            "unit": "iter/sec",
            "range": "stddev: 4.999094410820092e-7",
            "extra": "mean: 633.8181495744215 nsec\nrounds: 166362"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_serialization",
            "value": 148423.84615287912,
            "unit": "iter/sec",
            "range": "stddev: 0.000009690530541928334",
            "extra": "mean: 6.737461842687884 usec\nrounds: 11125"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 568015.4901292456,
            "unit": "iter/sec",
            "range": "stddev: 5.230095980928108e-7",
            "extra": "mean: 1.7605153686433115 usec\nrounds: 46751"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 600578.2329001277,
            "unit": "iter/sec",
            "range": "stddev: 5.145920039863319e-7",
            "extra": "mean: 1.6650620106078562 usec\nrounds: 42783"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 832352.835897533,
            "unit": "iter/sec",
            "range": "stddev: 4.1613970904204017e-7",
            "extra": "mean: 1.2014135795208671 usec\nrounds: 136912"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 836320.8071956071,
            "unit": "iter/sec",
            "range": "stddev: 4.752092881956639e-7",
            "extra": "mean: 1.19571340494714 usec\nrounds: 74935"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 647250.0566602286,
            "unit": "iter/sec",
            "range": "stddev: 4.999219131847502e-7",
            "extra": "mean: 1.5449979335033819 usec\nrounds: 89040"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 181325.78653212677,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010868775821371843",
            "extra": "mean: 5.514935405079978 usec\nrounds: 7369"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "fruch@scylladb.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "3d7b49ad1f6505faf97058a10525314fe3c802ce",
          "message": "feat(benchmarks): add vector benchmarks with SAI availability detection\n\nAdd pytest-benchmark suite for vector insert and ANN query operations\nwith automatic SAI availability detection. Update benchmark models and\nconftest to support vector-store container and shared Docker network.",
          "timestamp": "2026-04-14T17:58:30+03:00",
          "tree_id": "4d462baa22831480bd25a9a0e03c7945d01e9a3e",
          "url": "https://github.com/scylladb/coodie/commit/3d7b49ad1f6505faf97058a10525314fe3c802ce"
        },
        "date": 1776178762901,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 61705.96253004988,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018819729275247614",
            "extra": "mean: 16.20588933383893 usec\nrounds: 7491"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_instantiation",
            "value": 1626438.4853845977,
            "unit": "iter/sec",
            "range": "stddev: 2.8246853464701325e-7",
            "extra": "mean: 614.840345322703 nsec\nrounds: 196117"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_serialization",
            "value": 145774.0431112163,
            "unit": "iter/sec",
            "range": "stddev: 0.00003093909457743577",
            "extra": "mean: 6.859931841480611 usec\nrounds: 18501"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 558135.3172816132,
            "unit": "iter/sec",
            "range": "stddev: 4.879841614145144e-7",
            "extra": "mean: 1.7916802055646284 usec\nrounds: 39688"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 609239.5720339218,
            "unit": "iter/sec",
            "range": "stddev: 4.907185974764832e-7",
            "extra": "mean: 1.6413904248890796 usec\nrounds: 45681"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 865506.2969409513,
            "unit": "iter/sec",
            "range": "stddev: 3.49831623927356e-7",
            "extra": "mean: 1.1553930959652217 usec\nrounds: 154751"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 819032.1017090052,
            "unit": "iter/sec",
            "range": "stddev: 4.2169624495704003e-7",
            "extra": "mean: 1.2209533642373533 usec\nrounds: 71190"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 667586.6098309068,
            "unit": "iter/sec",
            "range": "stddev: 4.1314497119493715e-7",
            "extra": "mean: 1.4979329801915742 usec\nrounds: 88168"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 186997.2638846213,
            "unit": "iter/sec",
            "range": "stddev: 9.102620184700532e-7",
            "extra": "mean: 5.347671828059513 usec\nrounds: 6329"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "340979+fruch@users.noreply.github.com",
            "name": "fruch",
            "username": "fruch"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "ef93dcf848bd2726b511a5c1ec84e16b642357b7",
          "message": "perf: Phase 9 — model_construct() fast path, one-row driver shortcut, validate() chain\n\nAdapt the Python-RS driver to align with the upstream API changes, and introduce a `needs_row_validation` flag for improved model hydration path detection. Update documentation to clarify Phase 9 filter secondary index variance and add benchmark results. Optimize performance with a flip in default model construction and enhancements in execute_one_async. Apply consistent code styling and fix trailing whitespace in workflow files.",
          "timestamp": "2026-04-14T18:23:50+03:00",
          "tree_id": "3a56baccf757b8636eb1822156b4f96e29a4136c",
          "url": "https://github.com/scylladb/coodie/commit/ef93dcf848bd2726b511a5c1ec84e16b642357b7"
        },
        "date": 1776180284703,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 62462.05778257672,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015791756991361602",
            "extra": "mean: 16.009719107892437 usec\nrounds: 8384"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_instantiation",
            "value": 1621557.228665596,
            "unit": "iter/sec",
            "range": "stddev: 2.7728215563275313e-7",
            "extra": "mean: 616.6911548492897 nsec\nrounds: 172682"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_serialization",
            "value": 148159.21484473048,
            "unit": "iter/sec",
            "range": "stddev: 0.000028593332191034143",
            "extra": "mean: 6.7494958112999655 usec\nrounds: 18741"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 558840.1488064809,
            "unit": "iter/sec",
            "range": "stddev: 5.010795173189148e-7",
            "extra": "mean: 1.789420466900432 usec\nrounds: 46905"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 633750.1557567116,
            "unit": "iter/sec",
            "range": "stddev: 4.483621181943442e-7",
            "extra": "mean: 1.5779088824143608 usec\nrounds: 49266"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 846494.8722857499,
            "unit": "iter/sec",
            "range": "stddev: 4.0870398738110374e-7",
            "extra": "mean: 1.1813420644826207 usec\nrounds: 142593"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 837755.585277398,
            "unit": "iter/sec",
            "range": "stddev: 3.9361343913985755e-7",
            "extra": "mean: 1.1936655721237355 usec\nrounds: 76133"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 659351.1383517949,
            "unit": "iter/sec",
            "range": "stddev: 4.136541755725383e-7",
            "extra": "mean: 1.5166425624133113 usec\nrounds: 90164"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 171251.10421072057,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010819930842164716",
            "extra": "mean: 5.839378406398611 usec\nrounds: 7706"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "fruch@scylladb.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "124af0c586ca21b522382137de6951543bd5071e",
          "message": "test(benchmarks): add fair update benchmarks using QuerySet.update()\n\nAdd partial-update-fair and update-if-condition-fair benchmark groups that\nuse QuerySet.update() (1 roundtrip) instead of get()+doc.update() (2\nroundtrips) for apples-to-apples comparison with cqlengine.\n\nUltraworked with [Sisyphus](https://github.com/code-yeongyu/oh-my-openagent)\n\nCo-authored-by: Sisyphus <clio-agent@sisyphuslabs.ai>",
          "timestamp": "2026-04-14T19:43:46+03:00",
          "tree_id": "62235ec34d42260341e9ddb7c1186802697b8a3d",
          "url": "https://github.com/scylladb/coodie/commit/124af0c586ca21b522382137de6951543bd5071e"
        },
        "date": 1776185074287,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 62659.82385330891,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018502414797352164",
            "extra": "mean: 15.959189453533591 usec\nrounds: 8287"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_instantiation",
            "value": 1630227.348908919,
            "unit": "iter/sec",
            "range": "stddev: 2.5470831847511907e-7",
            "extra": "mean: 613.4113752105076 nsec\nrounds: 191205"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_serialization",
            "value": 148300.8844573125,
            "unit": "iter/sec",
            "range": "stddev: 0.000026733071148336872",
            "extra": "mean: 6.7430481190949605 usec\nrounds: 19140"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 545981.4971124461,
            "unit": "iter/sec",
            "range": "stddev: 6.600622141826079e-7",
            "extra": "mean: 1.8315638996719474 usec\nrounds: 47645"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 634039.2460888765,
            "unit": "iter/sec",
            "range": "stddev: 4.052341471164413e-7",
            "extra": "mean: 1.577189434516211 usec\nrounds: 65326"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 846044.8683479753,
            "unit": "iter/sec",
            "range": "stddev: 3.5591772039988e-7",
            "extra": "mean: 1.1819704100949684 usec\nrounds: 156202"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 821758.2231596382,
            "unit": "iter/sec",
            "range": "stddev: 3.8425804933616953e-7",
            "extra": "mean: 1.2169029427597657 usec\nrounds: 76017"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 666507.5057869905,
            "unit": "iter/sec",
            "range": "stddev: 5.097554005252044e-7",
            "extra": "mean: 1.5003581974958142 usec\nrounds: 136743"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 186439.74726748993,
            "unit": "iter/sec",
            "range": "stddev: 9.83335514439682e-7",
            "extra": "mean: 5.36366313866149 usec\nrounds: 7653"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "fruch@scylladb.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "869e29c3b8900ed9525aa4df5894844f52ac3978",
          "message": "feat(demo): add Dimension-10 Signal Graveyard vector search demo\n\nReplace the placeholder vector-search demo with a sci-fi themed\n'Dimension-10: The Signal Graveyard' demo using fastembed (BAAI/bge-small-en-v1.5,\nONNX-based, ~67MB, no torch) for real 384-dim semantic embeddings.\n\n- Rewrites models.py with DistressSignal (Vector + VectorIndex COSINE)\n- Rewrites seed.py with 30 distress signals across 5 categories\n- Rewrites main.py with fastembed-powered ANN search endpoint\n- Full dark-themed HTMX UI with threat badges and similarity scores\n- Drops sentence-transformers/torch dependency entirely\n- Uses own docker-compose.yml with scylladb/vector-store sidecar",
          "timestamp": "2026-04-14T22:31:03+03:00",
          "tree_id": "6992412fc3e8b357efb43831f68c206030c7a7a3",
          "url": "https://github.com/scylladb/coodie/commit/869e29c3b8900ed9525aa4df5894844f52ac3978"
        },
        "date": 1776195114570,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 63681.52180032267,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016431166449803513",
            "extra": "mean: 15.70314232024105 usec\nrounds: 7982"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_instantiation",
            "value": 1557048.54621665,
            "unit": "iter/sec",
            "range": "stddev: 3.2578912427746074e-7",
            "extra": "mean: 642.2407332319995 nsec\nrounds: 174521"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_serialization",
            "value": 145435.32945076862,
            "unit": "iter/sec",
            "range": "stddev: 0.000026545492003049654",
            "extra": "mean: 6.875908376434148 usec\nrounds: 19340"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 552491.7966216324,
            "unit": "iter/sec",
            "range": "stddev: 5.473540248618956e-7",
            "extra": "mean: 1.8099816252744079 usec\nrounds: 43266"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 596208.2279706053,
            "unit": "iter/sec",
            "range": "stddev: 4.413767990662765e-7",
            "extra": "mean: 1.6772663527369216 usec\nrounds: 47148"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 819527.5878525894,
            "unit": "iter/sec",
            "range": "stddev: 3.7718483406073693e-7",
            "extra": "mean: 1.2202151761849809 usec\nrounds: 134355"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 853501.5037177074,
            "unit": "iter/sec",
            "range": "stddev: 3.637243195826422e-7",
            "extra": "mean: 1.1716440986268568 usec\nrounds: 73068"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 622476.8050435473,
            "unit": "iter/sec",
            "range": "stddev: 4.126142267498305e-7",
            "extra": "mean: 1.6064855620283585 usec\nrounds: 84084"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 181677.01482950884,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010870841770014432",
            "extra": "mean: 5.504273619524351 usec\nrounds: 7642"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "fruch@scylladb.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "e058e11871790f4c936fc92e37c21599bce6732f",
          "message": "fix(cql_builder): remove duplicate param appends for collection ops and if_conditions in build_update\n\nDuring the rebase conflict resolution, build_update ended up appending\nparams in both the extraction block (which runs always) and the\nCQL-building loop (cache-miss only). This caused duplicate params for:\n- collection remove ops (params.append(value) in the loop)\n- put/setindex ops (params.extend([k, v]) in the loop)\n- if_conditions (params.extend(cond_params) in the cache-miss branch)\n\nRemove the stale param mutations from the CQL-building loop and the\ncache-miss if_conditions branch so params are only collected once in\nthe extraction block.\n\nAlso fix the extraction block to use _parse_if_conditions() instead of\nif_conditions.values() so that operator-bearing conditions (!=, >, <,\nIN) are expanded correctly.",
          "timestamp": "2026-04-14T23:46:31+03:00",
          "tree_id": "5be65fb82ddc5147701bb9c8e036f733863e0dcd",
          "url": "https://github.com/scylladb/coodie/commit/e058e11871790f4c936fc92e37c21599bce6732f"
        },
        "date": 1776199637692,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 63190.40523120995,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016706267547148488",
            "extra": "mean: 15.825187326162244 usec\nrounds: 8269"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_instantiation",
            "value": 1619797.8454780723,
            "unit": "iter/sec",
            "range": "stddev: 2.777272690405953e-7",
            "extra": "mean: 617.3609890837068 nsec\nrounds: 163908"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_serialization",
            "value": 145837.8756327254,
            "unit": "iter/sec",
            "range": "stddev: 0.000028900450017640568",
            "extra": "mean: 6.856929283023677 usec\nrounds: 18567"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 549048.5497490538,
            "unit": "iter/sec",
            "range": "stddev: 7.561933283260436e-7",
            "extra": "mean: 1.821332558763804 usec\nrounds: 44759"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 623061.4922552971,
            "unit": "iter/sec",
            "range": "stddev: 4.2957754511643823e-7",
            "extra": "mean: 1.6049780197140697 usec\nrounds: 53093"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 859146.5901244977,
            "unit": "iter/sec",
            "range": "stddev: 3.60120539813348e-7",
            "extra": "mean: 1.1639457241576103 usec\nrounds: 147211"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 857532.8458444831,
            "unit": "iter/sec",
            "range": "stddev: 3.690333285600449e-7",
            "extra": "mean: 1.1661360901170121 usec\nrounds: 80432"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 633707.8736163772,
            "unit": "iter/sec",
            "range": "stddev: 4.3574173199278385e-7",
            "extra": "mean: 1.5780141633609592 usec\nrounds: 119675"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 184816.79785906532,
            "unit": "iter/sec",
            "range": "stddev: 8.217850688044204e-7",
            "extra": "mean: 5.4107635863411305 usec\nrounds: 7673"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "fruch@scylladb.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "1e2743847fa09a04b4135b34c750de31ddf1b74b",
          "message": "test: add integration tests for TTL, batch writes, and advanced query features\n\n- add TTL/TIMESTAMP integration tests covering expiry, bulk update via QuerySet,\n  and Pydantic ValidationError handling when a TTL-expired column returns null\n- add batch write tests for empty batches and mixed-model batches\n- add advanced query tests covering token-based pagination, count/aggregate,\n  order_by, filtering on secondary index, and QuerySet chaining\n- fix sync_table calls in token tests and handle ValidationError from\n  model_validate() path (Acsylla driver) as valid proof of TTL expiry\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-04-14T23:46:46+03:00",
          "tree_id": "9b9b5d0e7fa90da6de2613ddd332b0cfce4cedde",
          "url": "https://github.com/scylladb/coodie/commit/1e2743847fa09a04b4135b34c750de31ddf1b74b"
        },
        "date": 1776199653219,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 61831.62955129755,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018299611640053954",
            "extra": "mean: 16.17295237497125 usec\nrounds: 8084"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_instantiation",
            "value": 1620852.8386768259,
            "unit": "iter/sec",
            "range": "stddev: 2.8019708460188784e-7",
            "extra": "mean: 616.9591564008639 nsec\nrounds: 189430"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_serialization",
            "value": 143604.16013930494,
            "unit": "iter/sec",
            "range": "stddev: 0.000026587882138368457",
            "extra": "mean: 6.963586563438957 usec\nrounds: 19633"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 550746.0717709508,
            "unit": "iter/sec",
            "range": "stddev: 4.5755980090878254e-7",
            "extra": "mean: 1.8157188062811802 usec\nrounds: 45001"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 606331.8706932914,
            "unit": "iter/sec",
            "range": "stddev: 4.28176720470186e-7",
            "extra": "mean: 1.6492618124404064 usec\nrounds: 49757"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 843784.3972640313,
            "unit": "iter/sec",
            "range": "stddev: 3.420789162445873e-7",
            "extra": "mean: 1.1851368705589926 usec\nrounds: 165536"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 841853.4304358743,
            "unit": "iter/sec",
            "range": "stddev: 3.673474504084959e-7",
            "extra": "mean: 1.1878552297188414 usec\nrounds: 78407"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 676649.2597997821,
            "unit": "iter/sec",
            "range": "stddev: 3.7898862676793487e-7",
            "extra": "mean: 1.477870529697906 usec\nrounds: 91828"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 183508.43307596748,
            "unit": "iter/sec",
            "range": "stddev: 0.00000100064351714922",
            "extra": "mean: 5.449340846292482 usec\nrounds: 7587"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "fruch@scylladb.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "614e547b4b5c84e7619066742107fc4520b1b1a7",
          "message": "fix(drivers): support python-rs-driver iter_current_page() API rename\n\nHandle the method rename from current_rows() to iter_current_page() in\npython-driver-rs for forward compatibility.\n\nUltraworked with [Sisyphus](https://github.com/code-yeongyu/oh-my-openagent)\n\nCo-authored-by: Sisyphus <clio-agent@sisyphuslabs.ai>",
          "timestamp": "2026-04-15T00:47:35+03:00",
          "tree_id": "21f1401b26553b184cf54c224726c3b266555aad",
          "url": "https://github.com/scylladb/coodie/commit/614e547b4b5c84e7619066742107fc4520b1b1a7"
        },
        "date": 1776203306771,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 63360.45094113357,
            "unit": "iter/sec",
            "range": "stddev: 0.000001581603295285857",
            "extra": "mean: 15.782715955242681 usec\nrounds: 8129"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_instantiation",
            "value": 1636125.1122788151,
            "unit": "iter/sec",
            "range": "stddev: 2.5560866028245484e-7",
            "extra": "mean: 611.2002025365821 nsec\nrounds: 191571"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_serialization",
            "value": 146478.76373857455,
            "unit": "iter/sec",
            "range": "stddev: 0.00002961391079217554",
            "extra": "mean: 6.826928180420287 usec\nrounds: 19911"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 575090.1996343968,
            "unit": "iter/sec",
            "range": "stddev: 4.914913363158465e-7",
            "extra": "mean: 1.7388576620428096 usec\nrounds: 42097"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 635938.1023539887,
            "unit": "iter/sec",
            "range": "stddev: 4.809194294412464e-7",
            "extra": "mean: 1.5724800830433021 usec\nrounds: 45765"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 855038.6874829505,
            "unit": "iter/sec",
            "range": "stddev: 3.751509212433956e-7",
            "extra": "mean: 1.169537723426041 usec\nrounds: 139025"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 880405.4578962207,
            "unit": "iter/sec",
            "range": "stddev: 4.1277967246222985e-7",
            "extra": "mean: 1.1358403006605131 usec\nrounds: 73175"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 668502.1200016335,
            "unit": "iter/sec",
            "range": "stddev: 4.2885206400764326e-7",
            "extra": "mean: 1.4958815687788043 usec\nrounds: 86641"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 165472.75935110543,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021569744372622983",
            "extra": "mean: 6.043290774393674 usec\nrounds: 7425"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "fruch@scylladb.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "d1e542ec7c714942288f62d0d1bf5ee7f7e392b6",
          "message": "feat(demos): add schema-migrations demo and fix migration base helpers\n\nAdd an interactive schema-migrations demo (Infinite Bazaar sci-fi theme)\nwith 6 versioned migrations, idempotent upgrade/downgrade, and a 13-step\ndemo.sh showcasing the coodie migrate CLI.\n\nAlso:\n- fix(migrations): add _get_all_columns(), column_exists(), index_exists()\n  to avoid ALLOW FILTERING on system_schema.columns queries; rewrite\n  _get_partition_key_columns() to filter by kind in Python\n- test(migrations): add kind field to mock pk_columns so _execute_side_effect\n  returns rows compatible with the new _get_all_columns() interface",
          "timestamp": "2026-04-15T06:45:06+03:00",
          "tree_id": "1b0d608a6c9fe76abe73104131e5b30dbb7cad2b",
          "url": "https://github.com/scylladb/coodie/commit/d1e542ec7c714942288f62d0d1bf5ee7f7e392b6"
        },
        "date": 1776224751739,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 61352.35774671001,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018516685887785512",
            "extra": "mean: 16.29929210102157 usec\nrounds: 7963"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_instantiation",
            "value": 1634397.6605071258,
            "unit": "iter/sec",
            "range": "stddev: 2.940473031692614e-7",
            "extra": "mean: 611.8462013031253 nsec\nrounds: 176679"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_serialization",
            "value": 140804.3526731852,
            "unit": "iter/sec",
            "range": "stddev: 0.00003663780150379349",
            "extra": "mean: 7.102053175309546 usec\nrounds: 18392"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 569104.5500852064,
            "unit": "iter/sec",
            "range": "stddev: 5.351298443161205e-7",
            "extra": "mean: 1.7571463799582692 usec\nrounds: 44323"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 627959.5000343851,
            "unit": "iter/sec",
            "range": "stddev: 4.4866920512003524e-7",
            "extra": "mean: 1.5924593862267282 usec\nrounds: 45391"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 831630.2129436749,
            "unit": "iter/sec",
            "range": "stddev: 4.960918700183944e-7",
            "extra": "mean: 1.2024575158956239 usec\nrounds: 149656"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 845276.4104427728,
            "unit": "iter/sec",
            "range": "stddev: 4.0514278271461567e-7",
            "extra": "mean: 1.1830449633347508 usec\nrounds: 73660"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 648293.6488357219,
            "unit": "iter/sec",
            "range": "stddev: 4.407038488236999e-7",
            "extra": "mean: 1.542510869566456 usec\nrounds: 81880"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 180522.07905885088,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010518871847299628",
            "extra": "mean: 5.539488605568276 usec\nrounds: 6275"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "Copilot",
            "username": "Copilot"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "388b7bdeff5650ce279e40de0ac79c6986481e1d",
          "message": "test(integration): add TTL and USING TIMESTAMP modifier tests (#215)\n\n* test(integration): add TTL and USING TIMESTAMP modifier tests\n\nAdd integration tests per §1.6 of the cqlengine test coverage plan:\n\n1. save(ttl=N) causes row to expire after TTL elapses\n2. __default_ttl__ in Settings applies default TTL to all saves\n3. save(timestamp=...) uses explicit write timestamp\n4. QuerySet.ttl(N) on bulk update causes updated cells to expire\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>\nAgent-Logs-Url: https://github.com/fruch/coodie/sessions/1722dec3-94bd-4d9a-a6f0-a5f66e53cfc9\n\n* test(integration): format ttl tests for pre-commit\n\nAgent-Logs-Url: https://github.com/scylladb/coodie/sessions/ce5939df-512d-4c8c-aaff-9a11ac80e0cd\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>\n\n---------\n\nCo-authored-by: copilot-swe-agent[bot] <198982749+Copilot@users.noreply.github.com>\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-04-15T06:47:09+03:00",
          "tree_id": "831bd5e4cf9c2824efe69b35a7aabb221f791f24",
          "url": "https://github.com/scylladb/coodie/commit/388b7bdeff5650ce279e40de0ac79c6986481e1d"
        },
        "date": 1776224880436,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 78192.15046726706,
            "unit": "iter/sec",
            "range": "stddev: 8.31506367214878e-7",
            "extra": "mean: 12.789007515768757 usec\nrounds: 5987"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_instantiation",
            "value": 1790666.6993045653,
            "unit": "iter/sec",
            "range": "stddev: 1.7530376604601577e-7",
            "extra": "mean: 558.4512184139942 nsec\nrounds: 116837"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_serialization",
            "value": 147915.12322540852,
            "unit": "iter/sec",
            "range": "stddev: 0.00004931663878448454",
            "extra": "mean: 6.760633924335753 usec\nrounds: 15505"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 574430.1999541058,
            "unit": "iter/sec",
            "range": "stddev: 3.1968140502985254e-7",
            "extra": "mean: 1.7408555470793408 usec\nrounds: 30979"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 644225.8155731169,
            "unit": "iter/sec",
            "range": "stddev: 3.970766689533367e-7",
            "extra": "mean: 1.5522507416291274 usec\nrounds: 29660"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 902631.8976517955,
            "unit": "iter/sec",
            "range": "stddev: 2.5867943258991487e-7",
            "extra": "mean: 1.1078713289453967 usec\nrounds: 78518"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 827774.3498239559,
            "unit": "iter/sec",
            "range": "stddev: 2.95014842889646e-7",
            "extra": "mean: 1.2080586940301685 usec\nrounds: 50414"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 709388.9109732714,
            "unit": "iter/sec",
            "range": "stddev: 2.867933823111818e-7",
            "extra": "mean: 1.4096639861877942 usec\nrounds: 76354"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 189547.4126544429,
            "unit": "iter/sec",
            "range": "stddev: 6.342049666514643e-7",
            "extra": "mean: 5.275724875353822 usec\nrounds: 6786"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "29139614+renovate[bot]@users.noreply.github.com",
            "name": "renovate[bot]",
            "username": "renovate[bot]"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "4e0aeaafbe7dde76480b3dc69e542e7689eeb82b",
          "message": "chore(deps): update codecov/codecov-action action to v6",
          "timestamp": "2026-04-15T13:33:15+03:00",
          "tree_id": "b196b785862d381cc26a0d4b462766d09f9723be",
          "url": "https://github.com/scylladb/coodie/commit/4e0aeaafbe7dde76480b3dc69e542e7689eeb82b"
        },
        "date": 1776249242127,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 54768.895339231036,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013609699036486965",
            "extra": "mean: 18.258538789328085 usec\nrounds: 7038"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_instantiation",
            "value": 1726435.313501278,
            "unit": "iter/sec",
            "range": "stddev: 2.2842789046639366e-7",
            "extra": "mean: 579.2281889623546 nsec\nrounds: 149477"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_serialization",
            "value": 144793.9108967924,
            "unit": "iter/sec",
            "range": "stddev: 0.00003546133461319031",
            "extra": "mean: 6.906367773385095 usec\nrounds: 17228"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 533015.9278879081,
            "unit": "iter/sec",
            "range": "stddev: 4.6898350293644956e-7",
            "extra": "mean: 1.876116543013134 usec\nrounds: 40972"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 593647.1124366606,
            "unit": "iter/sec",
            "range": "stddev: 4.681876431463389e-7",
            "extra": "mean: 1.6845024241681887 usec\nrounds: 40426"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 790371.3748826889,
            "unit": "iter/sec",
            "range": "stddev: 3.5777628455895475e-7",
            "extra": "mean: 1.2652280077177962 usec\nrounds: 97409"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 767890.4835883197,
            "unit": "iter/sec",
            "range": "stddev: 3.9649720096865956e-7",
            "extra": "mean: 1.3022690362394418 usec\nrounds: 61107"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 608997.8201418135,
            "unit": "iter/sec",
            "range": "stddev: 3.945109213974359e-7",
            "extra": "mean: 1.642042002329559 usec\nrounds: 75472"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 175787.91151534568,
            "unit": "iter/sec",
            "range": "stddev: 7.964385500856011e-7",
            "extra": "mean: 5.6886733073946525 usec\nrounds: 6927"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "58527c60e9c522d9d8e7aa739252640e38554238",
          "message": "fix(ci): add renovate[bot] and dependabot[bot] to allowed_bots in claude-code-review workflow\n\nAgent-Logs-Url: https://github.com/scylladb/coodie/sessions/3519dfa7-927c-4c4d-a777-fb93eaba453e\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-04-15T13:47:34+03:00",
          "tree_id": "5109575e728c280ddedb103f553a629252de2435",
          "url": "https://github.com/scylladb/coodie/commit/58527c60e9c522d9d8e7aa739252640e38554238"
        },
        "date": 1776250102240,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 78898.37607803527,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010135115180908616",
            "extra": "mean: 12.67453209697167 usec\nrounds: 9113"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_instantiation",
            "value": 1770781.5635128333,
            "unit": "iter/sec",
            "range": "stddev: 1.478601176071055e-7",
            "extra": "mean: 564.7223918551672 nsec\nrounds: 158857"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_serialization",
            "value": 155105.35801376397,
            "unit": "iter/sec",
            "range": "stddev: 0.00003146148297350488",
            "extra": "mean: 6.447230532882433 usec\nrounds: 18223"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 562005.6735006858,
            "unit": "iter/sec",
            "range": "stddev: 3.1590398120998143e-7",
            "extra": "mean: 1.7793414678024235 usec\nrounds: 44297"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 626654.639370427,
            "unit": "iter/sec",
            "range": "stddev: 4.1011911020661153e-7",
            "extra": "mean: 1.5957753077590824 usec\nrounds: 45164"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 902860.0089548038,
            "unit": "iter/sec",
            "range": "stddev: 1.9850626859436433e-7",
            "extra": "mean: 1.1075914206873005 usec\nrounds: 123320"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 822979.3584893751,
            "unit": "iter/sec",
            "range": "stddev: 3.3147784263130277e-7",
            "extra": "mean: 1.2150973043060962 usec\nrounds: 26227"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 717938.577370758,
            "unit": "iter/sec",
            "range": "stddev: 2.768441580572447e-7",
            "extra": "mean: 1.3928768163736376 usec\nrounds: 95175"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 189125.4691834834,
            "unit": "iter/sec",
            "range": "stddev: 6.573239086957498e-7",
            "extra": "mean: 5.287495144452662 usec\nrounds: 7620"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "29139614+renovate[bot]@users.noreply.github.com",
            "name": "renovate[bot]",
            "username": "renovate[bot]"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "89e5be5d54011c1b015a584df1ab5cb36b684b27",
          "message": "chore(deps): update actions/deploy-pages action to v5",
          "timestamp": "2026-04-15T13:48:16+03:00",
          "tree_id": "65d9d772a060a7046652f26db2d578577101d4b6",
          "url": "https://github.com/scylladb/coodie/commit/89e5be5d54011c1b015a584df1ab5cb36b684b27"
        },
        "date": 1776250141943,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 62043.819853176115,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017504779499372108",
            "extra": "mean: 16.117640763680487 usec\nrounds: 8120"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_instantiation",
            "value": 1570528.299229856,
            "unit": "iter/sec",
            "range": "stddev: 3.3944160650517974e-7",
            "extra": "mean: 636.7284183865852 nsec\nrounds: 160206"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_serialization",
            "value": 138819.6229834651,
            "unit": "iter/sec",
            "range": "stddev: 0.00003175240354831664",
            "extra": "mean: 7.203592536187126 usec\nrounds: 18382"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 569854.952589365,
            "unit": "iter/sec",
            "range": "stddev: 5.385139034508397e-7",
            "extra": "mean: 1.7548325156359494 usec\nrounds: 42601"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 614067.2624099805,
            "unit": "iter/sec",
            "range": "stddev: 4.4586928596568935e-7",
            "extra": "mean: 1.6284860978834472 usec\nrounds: 41109"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 834043.7458892912,
            "unit": "iter/sec",
            "range": "stddev: 3.9414396175906326e-7",
            "extra": "mean: 1.1989778772740027 usec\nrounds: 148083"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 853165.017588408,
            "unit": "iter/sec",
            "range": "stddev: 3.9182917944163797e-7",
            "extra": "mean: 1.1721061921017835 usec\nrounds: 68555"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 653643.434293035,
            "unit": "iter/sec",
            "range": "stddev: 4.273887103325197e-7",
            "extra": "mean: 1.5298860931443088 usec\nrounds: 87712"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 176373.3823078802,
            "unit": "iter/sec",
            "range": "stddev: 9.319498964072468e-7",
            "extra": "mean: 5.669789777316761 usec\nrounds: 7454"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "29139614+renovate[bot]@users.noreply.github.com",
            "name": "renovate[bot]",
            "username": "renovate[bot]"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "b710b551bbe14836b3a0619ab8912c6712c5a4cd",
          "message": "chore(deps): update pre-commit hooks (non-major)",
          "timestamp": "2026-04-15T13:48:50+03:00",
          "tree_id": "3914e8b146dc3ea54dbbeef44dd22df5207d6a74",
          "url": "https://github.com/scylladb/coodie/commit/b710b551bbe14836b3a0619ab8912c6712c5a4cd"
        },
        "date": 1776250182037,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 62593.169587363394,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018843732997446814",
            "extra": "mean: 15.976184088333573 usec\nrounds: 8409"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_instantiation",
            "value": 1607710.8880467867,
            "unit": "iter/sec",
            "range": "stddev: 3.138200194433482e-7",
            "extra": "mean: 622.0023807980198 nsec\nrounds: 195734"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_serialization",
            "value": 150109.16176501595,
            "unit": "iter/sec",
            "range": "stddev: 0.000007648014921365095",
            "extra": "mean: 6.661818560851209 usec\nrounds: 22779"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 621293.2302424789,
            "unit": "iter/sec",
            "range": "stddev: 5.066138447139394e-7",
            "extra": "mean: 1.6095459459774237 usec\nrounds: 65109"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 610120.7640291287,
            "unit": "iter/sec",
            "range": "stddev: 4.303960607430788e-7",
            "extra": "mean: 1.6390197792911987 usec\nrounds: 43682"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 856987.4027364416,
            "unit": "iter/sec",
            "range": "stddev: 3.6817055119988165e-7",
            "extra": "mean: 1.166878295768299 usec\nrounds: 156716"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 888732.1577544748,
            "unit": "iter/sec",
            "range": "stddev: 3.691965829844154e-7",
            "extra": "mean: 1.1251983978239983 usec\nrounds: 98242"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 651616.7522663266,
            "unit": "iter/sec",
            "range": "stddev: 3.878046151350882e-7",
            "extra": "mean: 1.5346444002889652 usec\nrounds: 100121"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 180829.2799339066,
            "unit": "iter/sec",
            "range": "stddev: 8.941301824422958e-7",
            "extra": "mean: 5.53007787436582 usec\nrounds: 7846"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "29139614+renovate[bot]@users.noreply.github.com",
            "name": "renovate[bot]",
            "username": "renovate[bot]"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "66b7b31799197677069550b6e34a36d45f743322",
          "message": "chore(deps): lock file maintenance",
          "timestamp": "2026-04-15T13:48:40+03:00",
          "tree_id": "e62df798c6fe03687c555d2424c2ad49685092c8",
          "url": "https://github.com/scylladb/coodie/commit/66b7b31799197677069550b6e34a36d45f743322"
        },
        "date": 1776250195703,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 71106.00280927827,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015974057658052168",
            "extra": "mean: 14.063510259214217 usec\nrounds: 8139"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_instantiation",
            "value": 2213289.403514807,
            "unit": "iter/sec",
            "range": "stddev: 1.580086612110685e-7",
            "extra": "mean: 451.8161964774933 nsec\nrounds: 175470"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_serialization",
            "value": 193084.14772545325,
            "unit": "iter/sec",
            "range": "stddev: 0.000007550338917807142",
            "extra": "mean: 5.179089074789828 usec\nrounds: 21510"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 728199.5482047362,
            "unit": "iter/sec",
            "range": "stddev: 3.269258219245898e-7",
            "extra": "mean: 1.3732499593900407 usec\nrounds: 61562"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 778914.3147183905,
            "unit": "iter/sec",
            "range": "stddev: 3.020921355178524e-7",
            "extra": "mean: 1.2838382619294153 usec\nrounds: 22116"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 1063398.5102248483,
            "unit": "iter/sec",
            "range": "stddev: 2.4420760127725736e-7",
            "extra": "mean: 940.3812309164857 nsec\nrounds: 162075"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 1049685.5418436367,
            "unit": "iter/sec",
            "range": "stddev: 4.205908934520959e-7",
            "extra": "mean: 952.6662606437635 nsec\nrounds: 75529"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 815872.8593385235,
            "unit": "iter/sec",
            "range": "stddev: 2.8380104186990104e-7",
            "extra": "mean: 1.225681169012975 usec\nrounds: 81780"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 230798.15039523985,
            "unit": "iter/sec",
            "range": "stddev: 5.607161285659309e-7",
            "extra": "mean: 4.332790355067875 usec\nrounds: 8958"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "copilot-swe-agent[bot]",
            "username": "Copilot"
          },
          "committer": {
            "email": "israel.fruchter@gmail.com",
            "name": "Israel Fruchter",
            "username": "fruch"
          },
          "distinct": true,
          "id": "3a212dceb03439e12b3f314cefcea68c6aebb21e",
          "message": "fix(ci): skip claude-code-review for bot-authored PRs\n\nAgent-Logs-Url: https://github.com/scylladb/coodie/sessions/89464566-e84d-4fb1-acbd-c8ab93485aa4\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>",
          "timestamp": "2026-04-15T23:28:03+03:00",
          "tree_id": "72db4df9f4613e9e81a8e941aea71f1b5d777594",
          "url": "https://github.com/scylladb/coodie/commit/3a212dceb03439e12b3f314cefcea68c6aebb21e"
        },
        "date": 1776284939521,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 63402.281587456404,
            "unit": "iter/sec",
            "range": "stddev: 0.000002163333448183789",
            "extra": "mean: 15.77230306169047 usec\nrounds: 8721"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_instantiation",
            "value": 1616529.6655540646,
            "unit": "iter/sec",
            "range": "stddev: 2.8396503237386944e-7",
            "extra": "mean: 618.6091237968408 nsec\nrounds: 190513"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_serialization",
            "value": 151471.00447178708,
            "unit": "iter/sec",
            "range": "stddev: 0.000009204967032139332",
            "extra": "mean: 6.60192360569088 usec\nrounds: 20080"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 631459.5210074659,
            "unit": "iter/sec",
            "range": "stddev: 4.3442526037827953e-7",
            "extra": "mean: 1.583632785209326 usec\nrounds: 60643"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 637805.6808625073,
            "unit": "iter/sec",
            "range": "stddev: 4.786459678363284e-7",
            "extra": "mean: 1.5678756555565574 usec\nrounds: 34887"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 858438.9735393965,
            "unit": "iter/sec",
            "range": "stddev: 3.5599441875123467e-7",
            "extra": "mean: 1.164905171857399 usec\nrounds: 150989"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 876886.8032359538,
            "unit": "iter/sec",
            "range": "stddev: 3.844857460778261e-7",
            "extra": "mean: 1.140398049451451 usec\nrounds: 77616"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 672971.3902433184,
            "unit": "iter/sec",
            "range": "stddev: 3.957116213589095e-7",
            "extra": "mean: 1.4859472698214433 usec\nrounds: 87559"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 188644.9405129627,
            "unit": "iter/sec",
            "range": "stddev: 8.050534396253074e-7",
            "extra": "mean: 5.300963796223759 usec\nrounds: 7734"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "198982749+Copilot@users.noreply.github.com",
            "name": "Copilot",
            "username": "Copilot"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "ca30015af6fe1aa6549e93f841de326c2b043a62",
          "message": "test(integration): add custom index name tests and update AcsyllaDriver coverage docs (#230)\n\nCo-authored-by: fruch <340979+fruch@users.noreply.github.com>\nCo-authored-by: copilot-swe-agent[bot] <198982749+Copilot@users.noreply.github.com>",
          "timestamp": "2026-04-16T01:05:18+03:00",
          "tree_id": "5ab93c59f842e6dfa890cdc3b4b840f4fceb8750",
          "url": "https://github.com/scylladb/coodie/commit/ca30015af6fe1aa6549e93f841de326c2b043a62"
        },
        "date": 1776290775235,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 64004.082551796586,
            "unit": "iter/sec",
            "range": "stddev: 0.000001699678100415804",
            "extra": "mean: 15.624003346829163 usec\nrounds: 8366"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_instantiation",
            "value": 1642481.7849245314,
            "unit": "iter/sec",
            "range": "stddev: 2.4057936371734873e-7",
            "extra": "mean: 608.8347579732508 nsec\nrounds: 169751"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_serialization",
            "value": 147682.29868727556,
            "unit": "iter/sec",
            "range": "stddev: 0.00000818596099510185",
            "extra": "mean: 6.7712922191003315 usec\nrounds: 20666"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 587278.5194238722,
            "unit": "iter/sec",
            "range": "stddev: 5.522177347187269e-7",
            "extra": "mean: 1.7027695836398253 usec\nrounds: 63216"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 620706.3643706475,
            "unit": "iter/sec",
            "range": "stddev: 4.5204259124613363e-7",
            "extra": "mean: 1.6110677405634943 usec\nrounds: 32964"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 832904.5956630845,
            "unit": "iter/sec",
            "range": "stddev: 4.161259119624343e-7",
            "extra": "mean: 1.200617700042691 usec\nrounds: 145943"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 894164.4916181274,
            "unit": "iter/sec",
            "range": "stddev: 3.965700625290151e-7",
            "extra": "mean: 1.1183624594512214 usec\nrounds: 73611"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 723453.2305105289,
            "unit": "iter/sec",
            "range": "stddev: 3.9120680175910686e-7",
            "extra": "mean: 1.382259360835692 usec\nrounds: 87866"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 185768.36495938752,
            "unit": "iter/sec",
            "range": "stddev: 9.092668488630863e-7",
            "extra": "mean: 5.3830478629589 usec\nrounds: 7417"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "29139614+renovate[bot]@users.noreply.github.com",
            "name": "renovate[bot]",
            "username": "renovate[bot]"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "d00f830d4ba4d1e8ab97a77764ba54f26e3af2b7",
          "message": "chore(deps): update scylladb/scylla docker tag to v2025.4.6 (#234)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2026-04-20T05:30:20Z",
          "tree_id": "0248aa02eec0cd53798084036d95e6802a7efc6b",
          "url": "https://github.com/scylladb/coodie/commit/d00f830d4ba4d1e8ab97a77764ba54f26e3af2b7"
        },
        "date": 1776663066273,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 55275.68268821546,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014219603125791242",
            "extra": "mean: 18.091137935654945 usec\nrounds: 7518"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_instantiation",
            "value": 1742975.475291142,
            "unit": "iter/sec",
            "range": "stddev: 2.316460144457631e-7",
            "extra": "mean: 573.7315379225073 nsec\nrounds: 159516"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_serialization",
            "value": 141054.79749758786,
            "unit": "iter/sec",
            "range": "stddev: 0.000008174690549748944",
            "extra": "mean: 7.089443377614296 usec\nrounds: 18332"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 564169.6393287139,
            "unit": "iter/sec",
            "range": "stddev: 4.5966330537142945e-7",
            "extra": "mean: 1.772516509732544 usec\nrounds: 56603"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 598545.6796432587,
            "unit": "iter/sec",
            "range": "stddev: 4.234071835748061e-7",
            "extra": "mean: 1.6707162611147965 usec\nrounds: 29869"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 819114.612519923,
            "unit": "iter/sec",
            "range": "stddev: 3.499084225971539e-7",
            "extra": "mean: 1.2208303755241303 usec\nrounds: 134391"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 830361.2939013918,
            "unit": "iter/sec",
            "range": "stddev: 3.806444636388668e-7",
            "extra": "mean: 1.204295054868915 usec\nrounds: 69726"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 709763.0338435459,
            "unit": "iter/sec",
            "range": "stddev: 3.738104897813529e-7",
            "extra": "mean: 1.408920938844543 usec\nrounds: 85339"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 177596.43361786907,
            "unit": "iter/sec",
            "range": "stddev: 7.227770892338366e-7",
            "extra": "mean: 5.630743701484914 usec\nrounds: 7343"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "29139614+renovate[bot]@users.noreply.github.com",
            "name": "renovate[bot]",
            "username": "renovate[bot]"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "412a322d77e05c969f4d4fdd7705be625ab6b3ba",
          "message": "chore(deps): update pre-commit hook astral-sh/ruff-pre-commit to v0.15.11 (#236)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2026-04-27T05:26:10Z",
          "tree_id": "fe5231edee7c7ff914aad23fadb4ee1b12d7b826",
          "url": "https://github.com/scylladb/coodie/commit/412a322d77e05c969f4d4fdd7705be625ab6b3ba"
        },
        "date": 1777267622863,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 62329.79704331757,
            "unit": "iter/sec",
            "range": "stddev: 0.000001923021915490943",
            "extra": "mean: 16.04369093814033 usec\nrounds: 8144"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_instantiation",
            "value": 1664624.3964919988,
            "unit": "iter/sec",
            "range": "stddev: 3.0312928895232285e-7",
            "extra": "mean: 600.7361192755453 nsec\nrounds: 191939"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_serialization",
            "value": 146604.7351934161,
            "unit": "iter/sec",
            "range": "stddev: 0.000010026448720945351",
            "extra": "mean: 6.821062080161987 usec\nrounds: 19507"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 596686.1964895473,
            "unit": "iter/sec",
            "range": "stddev: 5.165338019484562e-7",
            "extra": "mean: 1.6759227980859082 usec\nrounds: 61501"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 626160.9925886713,
            "unit": "iter/sec",
            "range": "stddev: 4.853701182740216e-7",
            "extra": "mean: 1.597033369750175 usec\nrounds: 31076"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 863560.4744789273,
            "unit": "iter/sec",
            "range": "stddev: 3.9287629310471594e-7",
            "extra": "mean: 1.1579964919114671 usec\nrounds: 139393"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 885621.2296065037,
            "unit": "iter/sec",
            "range": "stddev: 3.973536337323537e-7",
            "extra": "mean: 1.1291508904368932 usec\nrounds: 73497"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 748944.3661194994,
            "unit": "iter/sec",
            "range": "stddev: 3.9616648710875606e-7",
            "extra": "mean: 1.3352126609634485 usec\nrounds: 88098"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 178360.4175694254,
            "unit": "iter/sec",
            "range": "stddev: 9.750651558083173e-7",
            "extra": "mean: 5.606625133688969 usec\nrounds: 7480"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "29139614+renovate[bot]@users.noreply.github.com",
            "name": "renovate[bot]",
            "username": "renovate[bot]"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "4df74642879311f23ecbee064b45a15d580739db",
          "message": "chore(deps): update scylladb/scylla docker tag to v2025.4.7 (#237)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2026-04-27T09:27:22Z",
          "tree_id": "d104acb05231222f7586538b5f604afa9ac67e73",
          "url": "https://github.com/scylladb/coodie/commit/4df74642879311f23ecbee064b45a15d580739db"
        },
        "date": 1777282087663,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 63691.78034294642,
            "unit": "iter/sec",
            "range": "stddev: 0.000001551869740200234",
            "extra": "mean: 15.700613087207344 usec\nrounds: 8237"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_instantiation",
            "value": 1622797.996503232,
            "unit": "iter/sec",
            "range": "stddev: 2.422816686589745e-7",
            "extra": "mean: 616.2196417266827 nsec\nrounds: 162023"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_serialization",
            "value": 144860.82467962857,
            "unit": "iter/sec",
            "range": "stddev: 0.000007525119783111828",
            "extra": "mean: 6.903177599682874 usec\nrounds: 21205"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 601893.4863989049,
            "unit": "iter/sec",
            "range": "stddev: 4.657600359764326e-7",
            "extra": "mean: 1.6614235285763665 usec\nrounds: 62775"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 631198.7979430221,
            "unit": "iter/sec",
            "range": "stddev: 4.470922356015429e-7",
            "extra": "mean: 1.5842869207907924 usec\nrounds: 34574"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 851378.8648607462,
            "unit": "iter/sec",
            "range": "stddev: 3.931069099135872e-7",
            "extra": "mean: 1.17456521564411 usec\nrounds: 144030"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 883864.0203383182,
            "unit": "iter/sec",
            "range": "stddev: 3.7399949237212677e-7",
            "extra": "mean: 1.1313957543121036 usec\nrounds: 70943"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 738636.5481287026,
            "unit": "iter/sec",
            "range": "stddev: 4.0790236487618903e-7",
            "extra": "mean: 1.3538458156903397 usec\nrounds: 79593"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 182302.5178203735,
            "unit": "iter/sec",
            "range": "stddev: 8.906150334958845e-7",
            "extra": "mean: 5.485387760718264 usec\nrounds: 7631"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "29139614+renovate[bot]@users.noreply.github.com",
            "name": "renovate[bot]",
            "username": "renovate[bot]"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "4369147debd3445b3a0b411f034e911a9caaac20",
          "message": "chore(deps): update pre-commit hook astral-sh/ruff-pre-commit to v0.15.12 (#238)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2026-05-04T05:01:15Z",
          "tree_id": "eb292e320bd102b8b31f466af2f4c1ffbfe7d1e5",
          "url": "https://github.com/scylladb/coodie/commit/4369147debd3445b3a0b411f034e911a9caaac20"
        },
        "date": 1777870931965,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 81109.01298482367,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011307795329619826",
            "extra": "mean: 12.329086043583224 usec\nrounds: 9286"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_instantiation",
            "value": 1730651.1033600336,
            "unit": "iter/sec",
            "range": "stddev: 1.7965359375123676e-7",
            "extra": "mean: 577.8172146069851 nsec\nrounds: 163640"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_serialization",
            "value": 162121.9611498756,
            "unit": "iter/sec",
            "range": "stddev: 0.000010590516251976744",
            "extra": "mean: 6.168195800910266 usec\nrounds: 19290"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 624327.8032712999,
            "unit": "iter/sec",
            "range": "stddev: 3.1023491750328706e-7",
            "extra": "mean: 1.601722676389366 usec\nrounds: 58466"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 635221.010443288,
            "unit": "iter/sec",
            "range": "stddev: 3.0017723349941126e-7",
            "extra": "mean: 1.5742552333118696 usec\nrounds: 32723"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 887704.7295745041,
            "unit": "iter/sec",
            "range": "stddev: 2.4485111634683437e-7",
            "extra": "mean: 1.1265007008347487 usec\nrounds: 110583"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 893882.178289911,
            "unit": "iter/sec",
            "range": "stddev: 2.3437014087502136e-7",
            "extra": "mean: 1.1187156700149268 usec\nrounds: 73063"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 790903.0296344789,
            "unit": "iter/sec",
            "range": "stddev: 3.106761870065506e-7",
            "extra": "mean: 1.2643775058772462 usec\nrounds: 78865"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 187729.5694255496,
            "unit": "iter/sec",
            "range": "stddev: 5.797023374379818e-7",
            "extra": "mean: 5.326811343892115 usec\nrounds: 7352"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "29139614+renovate[bot]@users.noreply.github.com",
            "name": "renovate[bot]",
            "username": "renovate[bot]"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "c44071d887221fbcdaf3cd816618de0c1b852809",
          "message": "chore(deps): update pre-commit hook commitizen-tools/commitizen to v4.15.0 (#240)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2026-05-11T05:59:02Z",
          "tree_id": "714ade6b400ea351dc85dd9d9a2a6ff7c9852deb",
          "url": "https://github.com/scylladb/coodie/commit/c44071d887221fbcdaf3cd816618de0c1b852809"
        },
        "date": 1778479201262,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/bench_argus.py::test_coodie_argus_model_instantiation",
            "value": 62180.7334758498,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017117760999521937",
            "extra": "mean: 16.082151883724357 usec\nrounds: 8467"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_instantiation",
            "value": 1611785.5656546683,
            "unit": "iter/sec",
            "range": "stddev: 2.610864452290881e-7",
            "extra": "mean: 620.429926479596 nsec\nrounds: 173011"
          },
          {
            "name": "benchmarks/bench_raw_dc.py::test_raw_dc_model_serialization",
            "value": 145656.29764868712,
            "unit": "iter/sec",
            "range": "stddev: 0.000008435727986543345",
            "extra": "mean: 6.865477264923557 usec\nrounds: 20695"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_instantiation",
            "value": 588922.0287648654,
            "unit": "iter/sec",
            "range": "stddev: 5.532188620875236e-7",
            "extra": "mean: 1.6980176511605118 usec\nrounds: 60676"
          },
          {
            "name": "benchmarks/bench_serialization.py::test_coodie_model_serialization",
            "value": 611234.9875369851,
            "unit": "iter/sec",
            "range": "stddev: 5.095523354107191e-7",
            "extra": "mean: 1.63603200142317 usec\nrounds: 32780"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_serialization",
            "value": 839769.1360812433,
            "unit": "iter/sec",
            "range": "stddev: 3.9097048904969853e-7",
            "extra": "mean: 1.1908034685181086 usec\nrounds: 140985"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_instantiation",
            "value": 880327.7962137336,
            "unit": "iter/sec",
            "range": "stddev: 3.8408485720971755e-7",
            "extra": "mean: 1.1359405034135845 usec\nrounds: 78223"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_nested_udt_serialization",
            "value": 721417.8617031389,
            "unit": "iter/sec",
            "range": "stddev: 4.150303038920584e-7",
            "extra": "mean: 1.3861591916218683 usec\nrounds: 84948"
          },
          {
            "name": "benchmarks/bench_udt.py::test_coodie_udt_ddl_generation",
            "value": 185566.95775906954,
            "unit": "iter/sec",
            "range": "stddev: 9.21539892285838e-7",
            "extra": "mean: 5.388890414953872 usec\nrounds: 7574"
          }
        ]
      }
    ]
  }
}