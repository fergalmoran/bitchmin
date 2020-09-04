import jwtDecode from 'jwt-decode';

const isValidJwt = (jwt: string) => {
    if (!jwt || jwt.split('.').length < 3) {
        return false;
    }
    const data = JSON.parse(atob(jwt.split('.')[1]));
    const exp = new Date(data.exp * 1000); // JS deals with dates in milliseconds since epoch
    const now = new Date();
    return now < exp;
};

const decodeJwtToken = (jwt: string) => {
            if (jwt) {
                console.log('JwtDecoder', 'tokenChanged', jwt);

                    const decoded = jwtDecode(jwt);
                    console.log('JwtDecoder', 'decoded', decoded);
                    return decoded;

            }

}
export { isValidJwt, decodeJwtToken };
