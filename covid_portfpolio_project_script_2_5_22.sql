
SELECT *
FROM PortfolioProject..Coviddeaths
where continent is not NULL
order by 3,4


--SELECT *
--FROM PortfolioProject..Covidvacination
--order by 3,4

--select data that is going to be used

select location, date, total_cases, new_cases, total_deaths, population
from PortfolioProject..Coviddeaths
order by 1,2

--looking at Total cases vs Total deaths
--shows the chances of dying if you cotract covid in each country

select location, date, total_cases, total_deaths, (total_deaths/total_cases)*100 as death_percentage
from PortfolioProject..Coviddeaths
WHERE location like '%kingdom%'
order by 1,2

--Total cases vs Population
--To determine what percentage of the population has covid

select location, date, population,  total_cases, (total_cases/population)*100 as percent_of_infected_pop
from PortfolioProject..Coviddeaths
WHERE location like '%kingdom%'
order by 1,2

--Lookig for countries with highest infecction rates compared to population

select location, population, MAX(total_cases) as highest_infection_count, MAX((total_cases/population))*100 as percent_of_infected_pop
from PortfolioProject..Coviddeaths
--WHERE location like '%kingdom%'
group by location, population
order by percent_of_infected_pop desc

--Highest death count per population

select location, MAX(cast(total_deaths as int)) as total_death_count
from PortfolioProject..Coviddeaths
--WHERE location like '%kingdom%'
where continent is not NULL
group by location
order by total_death_count desc

--Highest death per continent

select continent, MAX(cast(total_deaths as int)) as total_death_count
from PortfolioProject..Coviddeaths
--WHERE location like '%kingdom%'
where continent is not NULL
group by continent
order by total_death_count desc

--Global numbers

select sum(new_cases) as total_newcases, sum(cast(new_deaths as int)) total_new_deaths, 
 sum(cast(new_deaths as int))/sum(new_cases)*100 as death_percentage
from PortfolioProject..Coviddeaths
--WHERE location like '%kingdom%'
where continent is not null
--group by date
order by 1,2

--total population vs population

select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
sum(cast(vac.new_vaccinations as int)) over (partition by dea.location order by dea.location, dea.date) as rolling_people_vacinated
--,(rolling_people_vacinated/population)*100
from PortfolioProject..Coviddeaths dea
join PortfolioProject..Covidvacination vac
     on dea.location = vac.location
	 and dea.date = vac.date
where dea.continent is not null
order by 2,3

-- Use CTE

with PopvsVac (continent, location, date, population, new_vacinations, rolling_people_vacinated)
as
(
select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
sum(convert(int,vac.new_vaccinations)) over (partition by dea.location order by dea.location, dea.date) as rolling_people_vacinated
--,(rolling_people_vacinated/population)*100
from PortfolioProject..Coviddeaths dea
join PortfolioProject..Covidvacination vac
     on dea.location = vac.location
	 and dea.date = vac.date
where dea.continent is not null
--order by 2,3
)
select *, (rolling_people_vacinated/population)*100
from PopvsVac


--Temp table

drop table if exists #percentage_population_vaccinated
Create table #percentage_population_vaccinated
(
continent nvarchar(255),
location nvarchar(255),
date datetime,
population numeric,
new_vacinations numeric,
rolling_people_vacinated numeric
)

insert into #percentage_population_vaccinated
select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
sum(convert(int,vac.new_vaccinations)) over (partition by dea.location order by dea.location, dea.date) as rolling_people_vacinated
--,(rolling_people_vacinated/population)*100
from PortfolioProject..Coviddeaths dea
join PortfolioProject..Covidvacination vac
     on dea.location = vac.location
	 and dea.date = vac.date
--where dea.continent is not null
--order by 2,3

select *, (rolling_people_vacinated/population)*100
from #percentage_population_vaccinated


--creating view to store data for later visualizations

 create view PopvsVac as
 select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
sum(convert(int,vac.new_vaccinations)) over (partition by dea.location order by dea.location, dea.date) as rolling_people_vacinated
--,(rolling_people_vacinated/population)*100
from PortfolioProject..Coviddeaths dea
join PortfolioProject..Covidvacination vac
     on dea.location = vac.location
	 and dea.date = vac.date
where dea.continent is not null
--order by 2,3

select *
from Pop