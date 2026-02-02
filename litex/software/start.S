.section .text
.global _start

_start:
    /* Set up stack pointer */
    la sp, _fstack
    
    /* Jump to C main */
    call main

    /* Hang if main returns */
    j .
