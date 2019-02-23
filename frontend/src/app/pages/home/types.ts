export class Iris {
    sepal_length: number = 5.0;
    sepal_width: number = 3.5;
    petal_length: number = 2.5;
    petal_width: number = 1.2;
}

export class ProbabilityPrediction {
    name: string;
    value: number;
}

export class SVCParameters {
    C: number = 2.0;
}

export class SVCResult {
    accuracy: number;
}