del perf.log
del perf.svg
python -m flamegraph -o perf.log tradewinds.py
C:\Strawberry\perl\bin\perl.exe ..\..\Perl\FlameGraph\flamegraph.pl .\perf.log > .\perf.svg
.\perf.svg
