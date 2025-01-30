        private class Token
        {
            private string Expression { get; set; }

            private double _value = double.NaN;

            internal double? Value 
            {
                get
                {
                    if (!double.IsNaN(_value) || double.TryParse(Expression, NumberStyles.Float, CultureInfo, out _value))
                    {
                        return _value;
                    }
                    else
                    {
                        return null;
                    }
                }
                set => _value = value ?? double.NaN; 
            }

            private Token(string expression)
            {
                Expression = expression;
            }
        }
