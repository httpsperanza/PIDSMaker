# Provfusion new GT

Orthrus ground truth update guided by the DARPA reports and REAPr. Audit logs were manually examined to identify and verify missing entities using multiple evidence sources—timestamp alignment, filename or command-line matching, file-path consistency, and causal dependencies—with cross-review among annotators.

New labels we added for Theia-e3 (+11 nodes), Clearscope-e3 (+8 nodes), Clearscope-e5 (+2 nodes).

| Dataset | UUID | Attribute | Timestamp |
|---|---|---|---|
| THEIA-E3 | ED35A9B7-0200-0000-0000-000020 | /home/admin/profile | 2018-04-12 12:57 |
| THEIA-E3 | 273847BC-0200-0000-0000-000020 | /home/admin/profile | 2018-04-12 12:57 |
| THEIA-E3 | D037D3BA-0200-0000-0000-000020 | /home/admin/profile | 2018-04-12 13:10 |
| THEIA-E3 | D237D6BA-0200-0000-0000-000020 | /home/admin/profile | 2018-04-12 13:10 |
| THEIA-E3 | EE35ABB7-0200-0000-0000-000020 | /home/admin/profile | 2018-04-12 12:57 |
| THEIA-E3 | 1D38E3BB-0200-0000-0000-000020 | /home/admin/profile | 2018-04-12 13:15 |
| THEIA-E3 | EC3598B7-0200-0000-0000-000020 | /home/admin/profile | 2018-04-12 12:57 |
| THEIA-E3 | 54387BBE-0200-0000-0000-000020 | /home/admin/profile | 2018-04-12 13:26 |
| THEIA-E3 | 223838BC-0200-0000-0000-000020 | /home/admin/profile | 2018-04-12 13:16 |
| THEIA-E3 | 62175519-0400-0000-0000-000020 | /bin/bash (-c ./texec) | 2018-04-13 14:06 |
| THEIA-E3 | 0100D00F-2925-2E00-0000-1889CA01 | /tmp/mozilla_admin0/jAG_iSHt.bin.part | 2018-04-13 14:06 |
| Clearscope-E3 | 00000000-0000-0000-0000-000028A44E | org.mozilla.fennec_firefox_dev | 2018-04-11 14:12 |
| Clearscope-E3 | 00000000-0000-0000-0000-00002740D6 | org.mozilla.fennec_firefox_dev | 2018-04-11 13:54 |
| Clearscope-E3 | 00000000-0000-0000-0000-0000279530 | 128.55.12.166:45525→166.199.230.185:80 | 2018-04-11 13:54 |
| Clearscope-E3 | 00000000-0000-0000-0000-0000274E9 | 128.55.12.166:46162→166.199.230.185:80 | 2018-04-11 14:12 |
| Clearscope-E3 | 00000000-0000-0000-0000-00002B1ADE | 128.55.12.166:46316→166.199.230.185:80 | 2018-04-11 14:20 |
| Clearscope-E3 | 00000000-0000-0000-0000-000027871D | 128.55.12.166:55331→111.82.111.27:80 | 2018-04-11 13:54 |
| Clearscope-E3 | 00000000-0000-0000-0000-0000274D0 | 128.55.12.166:55968→111.82.111.27:80 | 2018-04-11 14:11 |
| Clearscope-E3 | 00000000-0000-0000-0000-00002B1AB3 | 128.55.12.166:56122→111.82.111.27:80 | 2018-04-11 14:20 |
| Clearscope-E5 | 00000000-0000-0000-0000-0000F3D696 | org.mozilla.fennec_vagrant | 2019-05-17 11:57 |
| Clearscope-E5 | 516DD5D2-8D47-CB75-4EC4-82FF9B5054BB | /data/data/org.mozilla.fennec_vagrant/files/mozilla/profiles.ini | 2019-05-17 11:57 |


## Reference:

```
@inproceedings{yang2026beyond,
  title={Beyond Nodes vs. Edges: A Multi-View Fusion Framework for Provenance-Based Intrusion Detection},
  author={Yang, Fan and Xu, Binyan and Tang, Di and Zhang, Kehuan},
  booktitle={2026 IEEE Symposium on Security and Privacy (SP)},
  pages={3739--3758},
  year={2026},
  organization={IEEE}
}
```