#include <stdio.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_system.h"
#include "esp_spi_flash.h"

//#define DEBUG
//#define DEBUG_TRAP
#define ROUND_NUM (4)
#define FLAG_LEN  (16)

const long func4_table[] = {4225317655, 2809032755, 91827849, 2462969875};
const long func5_table[] = {1154738393, 1197026425, 4005351880, 4106543864};

//// flag 'Koit5uH@Rin9orou'
//const long func2_table[] = {4008446428, 1185497809, 205799423, 2678651991};
//const long hash_correct[] = {0xbe78fc5d, 0x1fc50ac7, 0x54577f21, 0x3f36d55d};

// flag 'Rin9oWoT@berun9o'
const long func2_table[] = {4008446428, 58150609, 205799423, 2678651991};
const long hash_correct[] = {0x5935f1de, 0xb63725e7, 0xdfa10069, 0x4e556f64};


void func1(unsigned long data[4])
{
	unsigned long temp[4];

	temp[0] = data[0] + data[0] * data[1];
	temp[1] = data[1] + data[1] * data[2];
	temp[2] = data[2] + data[2] * data[3];
	temp[3] = data[3] + data[3] * data[0];

	memcpy(data, temp, sizeof(temp));
}

void func2(unsigned long data[4])
{
	data[0] += func2_table[0];
	data[1] += func2_table[1];
	data[2] += func2_table[2];
	data[3] += func2_table[3];
}

void func3(unsigned long data[4])
{
	unsigned long temp[4];

#ifdef DEBUG_TRAP
	if (data[1] == 0) {
		printf("[DEBUG] Divide by zero\n");
		temp[0] = data[0] + data[0] * data[0];
	}
	else {
		temp[0] = data[0] + data[0] % data[1];
	}
#else
	temp[0] = data[0] + data[0] % data[1];
#endif
	temp[1] = data[1] + data[1] % data[2];
	temp[2] = data[2] + data[2] % data[3];
	temp[3] = data[3] + data[3] % data[0];

	memcpy(data, temp, sizeof(temp));
}

void func4(unsigned long data[4])
{
	data[0] -= func4_table[0];
	data[1] -= func4_table[1];
	data[2] -= func4_table[2];
	data[3] -= func4_table[3];
}

void func5(unsigned long data[4])
{
	data[0] ^= func5_table[0];
	data[1] ^= func5_table[1];
	data[2] ^= func5_table[2];
	data[3] ^= func5_table[3];
}

void (*functable[5])(unsigned long data[4]) = {func1, func2, func3, func4, func5};

void hashfunc(unsigned long data[4])
{
	for (int i = 0; i < ROUND_NUM; i++) {
		for (int j = 0; j < sizeof(functable) / sizeof(functable[0]); j++) {
#ifdef DEBUG
			printf("[DEBUG] state = %08lx %08lx %08lx %08lx\n", data[0], data[1], data[2], data[3]);
#endif
			functable[j](data);
		}
	}
}

void app_main()
{
	printf("### Flag Checker ###\n\n");

	printf("Input flag : ");

	char flag[FLAG_LEN * 2];
	int i = 0;
	while(i < sizeof(flag) - 1) {
		uint8_t ch;
		ch = fgetc(stdin);
		if (ch!=0xFF)
		{
			if (ch == 0x0a) {
				break;
			}
			fputc(ch, stdout);
			flag[i] = ch;
			i++;
		}
		vTaskDelay(1);
	}
	flag[i] = '\0';

	printf("\n");

#ifdef DEBUG
	printf("flag = %s\n", flag);
#endif

	bool valid = true;

	if (strlen(flag) != FLAG_LEN) {
		valid = false;
	}

	for (int i = 0; i < FLAG_LEN; i++) {
		if (flag[i] < ' ' || flag[i] > '~') {
			valid = false;
			break;
		}
	}

	if (valid) {
		unsigned long hash[4];
		memcpy(hash, flag, sizeof(hash));

		hashfunc(hash);

#ifdef DEBUG
		printf("[DEBUG] hash = %08lx %08lx %08lx %08lx\n", hash[0], hash[1], hash[2], hash[3]);
#endif

		if (hash[0] == hash_correct[0] && hash[1] == hash_correct[1] && hash[2] == hash_correct[2] && hash[3] == hash_correct[3]) {
			printf("Correct.\n");
			printf("Flag is TWCTF{%s}\n", flag);
		}
		else {
			printf("Wrong.\n");
		}
	}
	else {
		printf("Wrong.\n");
	}

	fflush(stdout);
	vTaskDelay(5 * (1000 / portTICK_PERIOD_MS));
	esp_restart();
}
