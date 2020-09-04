import axios, { AxiosRequestConfig, AxiosResponse } from 'axios';
import { AuthResult } from '@/models/';

import { UserLoginModel } from '@/models/userLoginModel';
import store from '@/store';
import { apiConfig } from './config';
import { Api } from './apiBase';

export class AuthApi extends Api {
  constructor(config: AxiosRequestConfig) {
    // NEVER FORGET THE SUPER
    super(config);
  }

  public login(user: UserLoginModel): Promise<AxiosResponse<AuthResult>> {
    return this.post('/auth/login/', user);
  }

  public register(user: UserLoginModel) {
    return this.post('/auth/register/', user);
  }
}
export const authApi = new AuthApi(apiConfig);
