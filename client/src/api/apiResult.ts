export interface ApiResult {
    status: string;
}

export interface DataApiResult<T> extends ApiResult {
    payload?: T;
}
