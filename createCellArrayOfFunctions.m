function cellArrayOfFunctions = createCellArrayOfFunctions(functionInput, functionName)
%CREATECELLARRAYOFFUNCTIONS Convert function input to standardized cell array format
%
%   cellArrayOfFunctions = createCellArrayOfFunctions(functionInput, functionName)
%   
%   This function takes various forms of function specifications and converts
%   them into a standardized cell array of function handles.
%
%   INPUTS:
%     functionInput - Can be:
%                     * Empty ([])
%                     * Single function handle (@func)
%                     * Cell array of function handles {@func1, @func2}
%                     * String/char array of function name
%                     * Structure with function field
%     functionName  - String specifying the type of function (e.g., 'OutputFcn')
%
%   OUTPUT:
%     cellArrayOfFunctions - Cell array of function handles, or empty cell array

% Initialize output
cellArrayOfFunctions = {};

% Handle empty input
if isempty(functionInput)
    return;
end

% Handle structure input (like from optimget default)
if isstruct(functionInput)
    if isfield(functionInput, functionName)
        functionInput = functionInput.(functionName);
        if isempty(functionInput)
            return;
        end
    else
        return;
    end
end

% Handle different types of function input
if isa(functionInput, 'function_handle')
    % Single function handle
    cellArrayOfFunctions = {functionInput};
    
elseif iscell(functionInput)
    % Already a cell array - validate contents
    cellArrayOfFunctions = {};
    for i = 1:length(functionInput)
        currentFunc = functionInput{i};
        if isa(currentFunc, 'function_handle')
            cellArrayOfFunctions{end+1} = currentFunc;
        elseif ischar(currentFunc) || isstring(currentFunc)
            % Convert string/char to function handle
            try
                funcHandle = str2func(currentFunc);
                cellArrayOfFunctions{end+1} = funcHandle;
            catch ME
                warning('createCellArrayOfFunctions:InvalidFunction', ...
                    'Could not convert "%s" to function handle: %s', ...
                    char(currentFunc), ME.message);
            end
        else
            warning('createCellArrayOfFunctions:InvalidType', ...
                'Skipping invalid function type at index %d', i);
        end
    end
    
elseif ischar(functionInput) || isstring(functionInput)
    % String or character array - convert to function handle
    try
        funcHandle = str2func(functionInput);
        cellArrayOfFunctions = {funcHandle};
    catch ME
        warning('createCellArrayOfFunctions:InvalidFunction', ...
            'Could not convert "%s" to function handle: %s', ...
            char(functionInput), ME.message);
    end
    
else
    % Unsupported type
    warning('createCellArrayOfFunctions:UnsupportedType', ...
        'Unsupported function input type: %s', class(functionInput));
end

end