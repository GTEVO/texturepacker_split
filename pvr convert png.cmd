@echo off
for /f "usebackq tokens=*" %%d in (`dir /s /b *.pvr *.pvr.ccz *.pvr.gz`) do (
    @echo on
    TexturePacker.exe "%%d" --sheet "%%~dpnd.png" --opt RGBA8888 --allow-free-size --algorithm Basic --shape-padding 0 --border-padding 0 --padding 0
)