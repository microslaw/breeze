import { KwargI } from "../../models/kwarg.model";

export function mapApiResponseToKwargs(apiResponse: any[]): KwargI[] {
  return apiResponse.map((kwarg) => ({
    key: kwarg.arg_name,
    value: kwarg.value,
    type: kwarg.datatype,
    source: kwarg.arg_source,
  }));
}
