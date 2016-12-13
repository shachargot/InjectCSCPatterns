//------------------------------------------------------------------------------
// Service routines for main
//------------------------------------------------------------------------------
#ifndef TRIGGER_SERVICE_H
#define TRIGGER_SERVICE_H
//------------------------------------------------------------------------------
#include <cstring> 
#include <stdio.h>
#include <iostream>

//set config file location
//std::string config_file = "~/TMB_trigInjector_config.ini";

//------------------------------------------------------------------------------
int flip_pid(int pid);
//------------------------------------------------------------------------------
void ck(std::string msg_string, int data_read, int data_expect); 
//------------------------------------------------------------------------------
int cks(std::string msg_string, int data_read, int data_expect); 
//------------------------------------------------------------------------------
void tok(std::string msg_string, double fdata_read, double fdata_expect, double tolerance, int &status); 
//------------------------------------------------------------------------------
int inquire(std::string test, std::string val, const int &minv, const int &maxv, const int &radix, int &now, std::string config_file_in = "~/TMB_trigInjector_config.ini"); 
//------------------------------------------------------------------------------
int inquir2(std::string test, std::string val, const int &minv, const int &maxv, const int &radix, int &num, int &now, std::string config_file_in = "~/TMB_trigInjector_config.ini"); 
//------------------------------------------------------------------------------
int inquirl(std::string test, std::string val, const long int &minv, const long int &maxv, const int &radix, long int &now, std::string config_file_in = "~/TMB_trigInjector_config.ini"); 
//------------------------------------------------------------------------------
void inquirb(std::string test, std::string val, bool &now, std::string config_file_in = "~/TMB_trigInjector_config.ini"); 
//------------------------------------------------------------------------------
void inquirs(std::string test, std::string val, std::string &now, std::string config_file_in = "~/TMB_trigInjector_config.ini"); 
//------------------------------------------------------------------------------
void bit_to_array(const int &idata, int iarray[], const int &n); 
//------------------------------------------------------------------------------------------
int arrayOr(int array[32]); 
//------------------------------------------------------------------------------------------
int *arrayAnd(int array1[32], int array2[32]); 
//------------------------------------------------------------------------------
void crc22a (
        long int	&din,		// 16 bit integer
        long int	&crc,		// 22 bit integer
        int			reset);
//------------------------------------------------------------------------------
void nextCRC22_D16(int din[16], int crc[22], int newcrc[22]);
//------------------------------------------------------------------------------
int count1s(int pat[6]);
//------------------------------------------------------------------------------------------------------------------------
#endif
//------------------------------------------------------------------------------
