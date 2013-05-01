function s = triangular_sample(a, b, c, n)
    s = arrayfun(@(u)uniform_to_triangular(a, b, c, u), [unifrnd(0, 1, n, 1)]);
end

function t = uniform_to_triangular(a, b, c, u)

    if u < (c - a) / (b - a)
        t = a + sqrt(u * (b - a) * (c - a));
    else
        t = b - sqrt((1 - u) * (b - a) * (b -c));
    end

end

