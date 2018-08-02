@echo off

set filename=%1

@echo #pragma once> %filename%.h
@echo #include "%filename%.h"> %filename%.cpp