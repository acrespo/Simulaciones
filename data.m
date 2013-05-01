# Generate a sample of 40 project sizes
1;

function s = value_to_project_size(u)

    if u <= 0.1
        s = 1;
    elseif u <= 0.85
        s = 2;
    else
        s = 3;
    end

end

function d = date_from_params(type, hours, price)
    d = 0;
end

function projects = generate_projects(count, type, size_a, size_b, size_c, price_c, price_a_factor, price_b_factor)

    price_a = price_c * (1 + price_a_factor);
    price_b = price_c * (1 + price_b_factor);

    projects = zeros(count, 3);

    for i = 1 : count
        hours = triangular_sample(size_a, size_b, size_c, 1);
        price = triangular_sample(price_a, price_b, price_c, 1);
        end_date = date_from_params(type, hours, price);

        projects(i,:) = [
            hours ;
            price ;
            end_date
            ];

    end

end

project_sizes = arrayfun(@value_to_project_size, unifrnd(0, 1, 40, 1));

# Display the resulting project sizes
figure(1);
hist(project_sizes, 0:4);

projects_per_size = histc(project_sizes, 1:3);

data = {};

man_hour_price = 220;
data.small = generate_projects(projects_per_size(1), 1, 500, 2000, 1400, man_hour_price * 1.3, -0.2, 0.1);
data.medium = generate_projects(projects_per_size(2), 2, 2000, 4500, 3200, man_hour_price, -0.1, 0.1);
data.big = generate_projects(projects_per_size(3), 3, 4500, 8000, 5300, man_hour_price * 1.2, -0.4, 0.2);

# Display small data

disp(data.small);

figure(2);
hist(data.small(:,1));

figure(3);
hist(data.small(:,2));

figure(4);
hist(data.small(:,3));

# Display medium data

disp(data.medium);

figure(5);
hist(data.medium(:,1));

figure(6);
hist(data.medium(:,2));

figure(7);
hist(data.medium(:,3));

# Display big data

disp(data.big);

figure(8);
hist(data.big(:,1));

figure(9);
hist(data.big(:,2));

figure(10);
hist(data.big(:,3));

# Save stats
save('stats.mat', 'data');
