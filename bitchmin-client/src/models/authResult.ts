import { User } from './user';

export interface AuthResult {
    accessToken: string;
    refreshToken: string;
    user: User;
}
