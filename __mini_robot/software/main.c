/* robot motor driver program
 *
 * mcu : msp430g2452
 * ccs version : 5.5.0.00077
 * operating system : windows 10 64bit
 * author : caoliang
 * last update : 2015_08_09
 */

#include <msp430.h> 

#define CPU_F ((double)8000000)
#define delayus(x) __delay_cycles((long)(CPU_F*(double)x/1000000.0))
#define delayms(x) __delay_cycles((long)(CPU_F*(double)x/1000.0))
#define delays(x)  __delay_cycles((long)(CPU_F*(double)x/1.0))

#define MDOWN   TA0CCR1     //1.2
#define MUP     TA0CCR2


int main(void){
    unsigned int i = 0;

    WDTCTL = WDTPW | WDTHOLD;   /* Stop watchdog timer */

    BCSCTL1 = CALBC1_8MHZ;      /* Set range */
    DCOCTL = CALDCO_8MHZ;

    /*  timer A0 configuration
     *
     *  CCR 600 - 2700
     *	MID	1600
     */

    /* Timer A clock source -> SMCLK (1MHz), divider -> 8 , mode -> Up to CCR0 */
    TA0CTL = TASSEL_2 + ID_3 + MC_1;

    TA0CCR0 = 20000;            /* 20ms */
    TA0CCTL1 = OUTMOD_6;        /* PWM output mode: 6 -> PWM toggle/set */
    TA0CCTL2 = OUTMOD_6;
    MDOWN = 1650;
    MUP = 1650;

    /*
     * GPIO configuration
     *
     * PIN4 :  P1.2 -> TA0.1
     * PIN6 :  P1.4 -> TA0.2	/down
     */
    P1DIR = BIT2 + BIT4;
    P1SEL = BIT2 + BIT4;
    P1SEL2 = BIT4;
    delayms(3000);

    for (i = 0; i<500; i++){
        delayms(4);
        MUP += 1;
    }
    for (i = 0; i<280; i++){
        delayms(3);
        MDOWN -= 1;
	}
	/*********************/

	while(1){
        for (i = 0;i<1000;i++){
            delayms(2);
            MUP -= 1;
        }
        for (i = 0;i<560;i++){
            delayms(2);
            MDOWN += 1;
        }
        for (i = 0;i<1000;i++){
            delayms(2);
            MUP += 1;
        }
        for (i = 0;i<560;i++){
            delayms(2);
            MDOWN -= 1;
        }
    }
}
