#define SDL_MAIN_HANDLED
#if defined(__psp2__) || defined(__vita__)
#include <SDL2/SDL.h>
#include <psp2/kernel/processmgr.h>
#include <sys/stat.h>
int _newlib_heap_size_user = 32 * 1024 * 1024; /* 32 MB user heap */
#elif __has_include(<SDL2/SDL.h>)
#include <SDL2/SDL.h>
#else
#include <SDL.h>
#endif

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "host.h"
#include "mem.h"
#include "platform/gfx.h"
#include "platform/input.h"
#include "platform/timer.h"

int game_main(void);   /* game/flow.c: port of main() at 0000:07b3 */

int main(int argc, char **argv)
{
#if defined(__psp2__) || defined(__vita__)
    const char *dir = "ux0:data/TestDrive2";
    int scale = 1;
    mkdir("ux0:data", 0777);
    mkdir("ux0:data/TestDrive2", 0777);
    struct stat st;
    if (stat("ux0:data/TestDrive2/TD2EGA.EXE", &st) == 0 || stat("ux0:data/TestDrive2/td2ega.exe", &st) == 0) {
        dir = "ux0:data/TestDrive2";
    } else if (stat("app0:Game/TD2EGA.EXE", &st) == 0 || stat("app0:Game/td2ega.exe", &st) == 0) {
        dir = "app0:Game";
    } else {
        dir = "ux0:data/TestDrive2";
    }
#else
    const char *dir = "Game";
    int scale = 3;
#endif
    bool check = false;
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "--game-dir") && i + 1 < argc) dir = argv[++i];
        else if (!strcmp(argv[i], "--scale") && i + 1 < argc) scale = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--check")) check = true;
        else if (!strcmp(argv[i], "--frame-rate") && i + 1 < argc) host_set_frame_rate(atoi(argv[++i]));
        else {
            fprintf(stderr, "usage: %s [--game-dir DIR] [--scale N] [--frame-rate FPS] [--check]\n", argv[0]);
            return 2;
        }
    }

    char exe_path[1024];
    snprintf(exe_path, sizeof exe_path, "%s/%s", dir, TD_EXE_NAME);
    char err[256];
    if (!mem_load_exe(exe_path, err, sizeof err)) {
        /* Try lowercase */
        snprintf(exe_path, sizeof exe_path, "%s/td2ega.exe", dir);
        if (!mem_load_exe(exe_path, err, sizeof err)) {
            fprintf(stderr, "%s\n", err);
#if defined(__psp2__) || defined(__vita__)
            char msg[512];
            snprintf(msg, sizeof msg,
                "Could not find Test Drive II game data!\n\n"
                "Please copy original DOS game files\n"
                "(TD2EGA.EXE, CARS.DAT, SCENES.DAT, etc.) into:\n"
                "ux0:data/TestDrive2/\n\n"
                "Details: %s", err);
            SDL_ShowSimpleMessageBox(SDL_MESSAGEBOX_ERROR, "Test Drive II", msg, NULL);
#else
            SDL_ShowSimpleMessageBox(SDL_MESSAGEBOX_ERROR, "Test Drive II", err, NULL);
#endif
            return 1;
        }
    }
    if (check) {
        printf("%s ok (%s): image %u bytes at %04X:0000, DGROUP %04X\n", TD_EXE_NAME, TD_VARIANT_NAME,
               mem_image_size, LOAD_SEG, DGROUP);
        return 0;
    }

    if (!host_init(dir, scale)) return 1;
    gfx_init();      /* EGA model, frame source */
    timer_init();    /* host tick handler, timer routines */
    input_init();    /* INT 9 handler, getkey code pointers */
    int rc = game_main();
    host_shutdown();
    return rc;
}
